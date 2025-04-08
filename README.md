# Microsoft-Data-AI-Hack-2025

This repository highlights our solution submission for the Microsoft Data + AI Hack, held in Kenya.

# AI-Powered KRA Tax Return Automation Solution

![KRA Tax Automation](static/images/kra-logo.png) *An intelligent system for automating P9 form processing and tax return submissions*

## 📌 Overview

This solution automates Kenya Revenue Authority (KRA) tax return processing by:

1. **AI-Powered Extraction**: Uses Azure Document Intelligence to extract data from P9 forms
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



