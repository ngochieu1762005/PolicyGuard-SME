PolicyGuard SME

PolicyGuard SME is a demo web application that helps small and medium-sized enterprises understand how new policy or banking-related requirements may affect their business documents, loan renewal process, tax preparation, and compliance tasks.

The system allows users to select an SME profile and a sample policy document, then generates an impact analysis with a risk level, explanation, and suggested action checklist. The goal of this project is to make policy information easier to understand and help SMEs prepare required documents earlier.

This project was developed as a hackathon prototype. It uses sample data and a transparent rule-based scoring approach to demonstrate the main workflow. It is not intended to replace legal, tax, or financial advice.

Main Features
Select an SME profile from sample data
Select a policy or requirement document
Analyze how the policy affects the selected SME
Generate an impact score and risk level
Show reasons behind the result
Suggest an action checklist for the SME
Display the result in a simple Streamlit dashboard
Project Structure
policyguard_sme_project/
├── app.py
├── requirements.txt
├── run_app.bat
├── run_app.sh
├── data/
│   ├── sme_profiles.csv
│   ├── policies.csv
│   ├── rules.json
│   └── source_references.csv
├── sample_documents/
│   ├── policy_loan_renewal.txt
│   ├── policy_e_invoice.txt
│   └── policy_sme_support.txt
├── src/
│   └── analyzer.py
└── docs/
    ├── data_notes.md
    └── hackathon_plan.md
How to Run
1. Clone the project
git clone https://github.com/ngochieu1762005/PolicyGuard-SME
cd policyguard_sme_project
2. Install dependencies
python -m pip install -r requirements.txt
3. Run the application
python -m streamlit run app.py

The application will open in your browser at:

http://localhost:8501
Run on Windows

You can also run the project using:

run_app.bat
Run on Linux or macOS
bash run_app.sh
Demo Workflow
Open the Streamlit application.
Choose an SME profile from the sidebar.
Choose a policy document.
Run the analysis.
Review the impact score, risk level, explanation, and recommended action checklist.

Example:

SME: Demo Retail Company
Policy: Loan renewal document requirement
Result: High impact
Reason: The SME has an active loan and missing cash flow documents.
Recommended action: Prepare cash flow report, revenue proof, and contact the bank before renewal.
Notes

The data used in this project is sample data for demonstration only. It does not contain real banking customer information or confidential business data.