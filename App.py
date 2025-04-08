from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
import re
import PyPDF2
from io import BytesIO
import os
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import smtplib
from email.mime.text import MIMEText
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize data stores
users = {
    "A002067195Z": {
        "password": generate_password_hash("default123"),
        "email": "user@example.com",
        "name": "MR ARESMUS JEDI MWAJEDI"
    }
}

reset_tokens = {}

# Configuration - using environment variables
AZURE_FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
AZURE_FORM_RECOGNIZER_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
CUSTOM_MODEL_ID = os.getenv("CUSTOM_MODEL_ID")
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME", "p9submissions")

# Initialize Azure clients
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
document_analysis_client = DocumentAnalysisClient(
    endpoint=AZURE_FORM_RECOGNIZER_ENDPOINT,
    credential=AzureKeyCredential(AZURE_FORM_RECOGNIZER_KEY))

class P9FormData:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def extract_p9_data(pdf_content):
    """Fallback method if Azure is not available"""
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content))
        text = "\n".join([page.extract_text() for page in pdf_reader.pages])

        def extract(regex, default=""):
            match = re.search(regex, text)
            return match.group(1).strip() if match else default

        return P9FormData(
            employer_vote=extract(r"Employer \(Vote\):\s*([^\n]+)"),
            employer_pin=extract(r"Employer Tax-PIN:\s*([^\n]+)"),
            employee_name=extract(r"Tax Payer's Name:\s*([^\n]+)"),
            employee_number=extract(r"Payroll-Number:\s*(\d+)"),
            id_number=extract(r"ID-Number:\s*(\d+)"),
            kra_pin=extract(r"Tax-PIN:\s*([^\s]+)"),
            taxable_pay=float(extract(r"SubTotals\s*([\d,]+\.\d{2})", "0").replace(",", "")),
            total_paye=float(extract(r"Total PAYE = ([\d,]+\.\d{2})", "0").replace(",", "")),
            total_mpr=float(extract(r"MPR Value\s*[\d\.]+\s*[\d\.]+\s*([\d,]+\.\d{2})", "0").replace(",", "")))
    except Exception as e:
        raise ValueError(f"Error parsing P9 form: {str(e)}")

def analyze_p9_with_azure(pdf_content):
    """Analyze P9 form using Azure Document Intelligence"""
    try:
        poller = document_analysis_client.begin_analyze_document(
            model_id=CUSTOM_MODEL_ID,
            document=BytesIO(pdf_content))
        result = poller.result()
        
        extracted_data = {}
        for kv_pair in result.key_value_pairs:
            if kv_pair.key and kv_pair.value:
                extracted_data[kv_pair.key.content] = kv_pair.value.content
        
        return P9FormData(
            employer_vote=extracted_data.get("Employer Vote", ""),
            employer_pin=extracted_data.get("Employer Tax-PIN", ""),
            employee_name=extracted_data.get("Tax Payer's Name", ""),
            employee_number=extracted_data.get("Payroll-Number", ""),
            id_number=extracted_data.get("ID-Number", ""),
            kra_pin=extracted_data.get("Tax-PIN", ""),
            taxable_pay=float(extracted_data.get("Subtotals", "0").replace(",", "")),
            total_paye=float(extracted_data.get("Total PAYE", "0").replace(",", "")),
            total_mpr=float(extracted_data.get("MPR Value", "0").replace(",", "")))
    except Exception as e:
        app.logger.error(f"Azure analysis failed: {str(e)}")
        raise

    



def save_to_blob_storage(data):
    """Save P9 data to Azure Blob Storage"""
    try:
        # Get the container client
        container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)
        
        # Create a unique blob name
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        blob_name = f"p9_{data['kra_pin']}_{timestamp}.json"
        
        # Upload the JSON data
        container_client.upload_blob(
            name=blob_name,
            data=json.dumps(data),
            overwrite=True)
        
        return True
    except Exception as e:
        app.logger.error(f"Error saving to blob storage: {str(e)}")
        return False

def send_reset_email(email, token):
    print(f"Password reset link for {email}: http://localhost:5000/reset-password?token={token}")
    return True

# Sample files endpoint
@app.route('/samples/<filename>')
def download_sample(filename):
    samples_dir = os.path.join(app.root_path, 'static', 'samples')
    return send_from_directory(samples_dir, filename)

@app.route('/')
def home():
    session['current_step'] = 1
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        kra_pin = data.get('kra_pin', '').strip().upper()
        password = data.get('password', '').strip()

        # Demo validation - accept any password with 6+ characters
        if len(password) < 6:
            return jsonify({
                "success": False,
                "error": "Password must be at least 6 characters"
            }), 400

        # In demo mode, we accept any KRA PIN and create user if not exists
        if kra_pin not in users:
            users[kra_pin] = {
                "password": generate_password_hash(password),
                "email": f"{kra_pin.lower()}@example.com",
                "name": "Demo User"
            }

        session['user'] = kra_pin
        session['current_step'] = 2
        
        return jsonify({
            "success": True,
            "redirect": url_for('review')
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/request-reset', methods=['POST'])
def request_reset():
    email = request.form.get('email')
    # Find user by email
    user = next((k for k, v in users.items() if v['email'] == email), None)
    
    if user:
        token = secrets.token_urlsafe(32)
        reset_tokens[token] = user
        if send_reset_email(email, token):
            return jsonify({"success": True})
    
    return jsonify({"success": False, "error": "Email not found"}), 404

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        token = request.args.get('token')
        if token in reset_tokens:
            return render_template('reset_password.html', token=token)
        return redirect(url_for('home'))
    
    # Handle POST request
    token = request.form.get('token')
    new_password = request.form.get('password')
    
    if token in reset_tokens and len(new_password) >= 6:
        kra_pin = reset_tokens[token]
        users[kra_pin]['password'] = generate_password_hash(new_password)
        del reset_tokens[token]
        return jsonify({"success": True, "redirect": url_for('home')})
    
    return jsonify({"success": False, "error": "Invalid token or password too short"}), 400

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        try:
            pdf_content = file.read()
            
            # Try Azure Document Intelligence first, fallback to local parser
            try:
                form_data = analyze_p9_with_azure(pdf_content)
            except Exception as azure_error:
                app.logger.warning(f"Azure analysis failed, falling back to local parser: {azure_error}")
                form_data = extract_p9_data(pdf_content)
            
            session['p9_data'] = form_data.__dict__
            session['current_step'] = 1
            
            return jsonify({
                "success": True,
                "kra_pin": form_data.kra_pin,
                "current_step": 1
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Handle GET request
    return render_template('upload.html')

@app.route('/review')
def review():
    if 'user' not in session or 'p9_data' not in session:
        return redirect(url_for('home'))
    
    session['current_step'] = 2
    return render_template('review.html', 
                         data=session['p9_data'],
                         user=users.get(session['user']))
                         
@app.route('/submit', methods=['POST'])
def submit():
    if 'user' not in session or 'p9_data' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    # Save to Azure Blob Storage instead of Fabric
    submission_success = save_to_blob_storage(session['p9_data'])
    
    if not submission_success:
        return jsonify({"error": "Failed to save to storage"}), 500
    
    session['current_step'] = 3
    session.pop('p9_data', None)
    return jsonify({"success": True, "redirect": url_for('submit_page')})

@app.route('/download-template')
def download_template():
    try:
        # Ensure the file exists in your samples directory
        template_path = os.path.join(app.root_path, 'static', 'samples', 'IT1_Individual_Resident_Return_XLS.xls')
        
        if not os.path.exists(template_path):
            raise FileNotFoundError("Template file not found")
            
        return send_from_directory(
            directory=os.path.join(app.root_path, 'static', 'samples'),
            path='IT1_Individual_Resident_Return_XLS.xls',
            as_attachment=True,
            download_name='KRA_IT1_Template.xls'  # Custom download filename
        )
    except Exception as e:
        app.logger.error(f"Template download failed: {str(e)}")
        return jsonify({"error": "Failed to download template"}), 500

@app.route('/submit-page')
def submit_page():
    if 'user' not in session:
        return redirect(url_for('home'))
    return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True)