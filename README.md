# TaxPilot

This repository highlights our solution submission for the Microsoft Data + AI Hack, held in Kenya.

## 📌 Project Overview

TaxPilot is an advanced, AI-powered system designed to simplify and automate tax return filing in Kenya. This solution harnesses Microsoft Fabric and Azure services to provide a secure, accurate, and user-friendly experience for employed individuals to meet their tax obligations to the Kenya Revenue Authority (KRA) in a prompt and hassle-free manner. By leveraging AI for data extraction, validation, and submission, TaxPilot reduces errors, ensures compliance, and significantly improves the efficiency of tax filing.

![image](https://github.com/user-attachments/assets/075b0a17-0710-486f-aa05-34c950e1796d) 
*An intelligent system for automating P9 form processing and tax return submissions*

The following capabilities are implemented in TaxPilot:

1. **AI-Powered Data Extraction**: Uses Azure Document Intelligence to extract data from P9 forms
2. **Automated Workflow**: Guides users through upload, verification, and submission
3. **Secure Storage**: Saves processed data to Azure Blob Storage
4. **Tax Planning**: Provides analytics through Power BI integration

## 🛠 Key Technologies

| Component               | Technology Used               |
|-------------------------|-------------------------------|
| Form Processing         | Azure Document Intelligence   |
| Cloud Storage           | Azure Blob Storage            |
| Web Framework           | Python Flask                  |
| Frontend                | Bootstrap 5 + Jinja2          |
| Data Analytics          | Microsoft Fabric/Power BI     |
| Deployment              | Docker + Azure App Service    |

## 🚀 Features

- **Smart P9 Processing**: 
  - Custom-trained AI model for Kenyan P9 forms
  - Fallback to traditional PDF parsing if AI fails
- **User-Friendly Portal**:
  - Step-by-step submission workflow
  - Real-time data validation
- **Enterprise-Grade Security**:
  - Azure AD authentication
  - Encrypted data storage
- **Reporting Dashboard**:
  - Tax liability visualizations
  - Historical submission tracking

## Workflow Summary

The following steps are followed while using TaxPilot:

1. **User Uploads P9 Form**: Forms are securely uploaded to Azure Blob Storage.
2. **OCR & Data Validation**: AI extracts and validates P9 data.
3. **Excel/Submission Generation**: Outputs a KRA-compliant Excel or submits directly in a simulated environment.
4. **User Review & Approval**: Notifies user for manual review or corrections if needed.
5. **Post-Submission Insights**: Stores submission records and generates analytics.

A detailed documentation outlining the architecture, workflow, and analytics pipeline of TaxPilot can be found [here](https://github.com/faithhunja/Microsoft-Data-AI-Hack-2025/blob/main/taxPilot-follow-through.md).