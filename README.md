# PolicyGuard SME RAG

PolicyGuard SME is a modern demo web application for small and medium-sized enterprises. It helps SMEs understand how policy, tax, invoice, and banking-related requirements may affect loan renewal, business documents, and compliance tasks.

This version includes a simple RAG chatbot. The app retrieves relevant policy context from the local document folder, then uses an OpenAI model if an API key is available. If no API key is provided, the app still runs with a local fallback answer.

## Main Features

- White, modern Streamlit web interface
- SME profile selection
- Policy document selection
- Custom policy text input
- Local RAG retrieval from policy documents
- Optional OpenAI-powered chatbot
- Impact score and risk level
- Explanation of why a policy affects the SME
- Action checklist for required documents
- Markdown report export
- Public source references included in the dataset

## Project Structure

```text
PolicyGuard-SME-RAG/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── run_app.bat
├── run_app.sh
├── data/
│   ├── sme_profiles.csv
│   ├── rules.json
│   └── sources.csv
├── documents/
│   ├── 01_sme_support_law.md
│   ├── 02_e_invoice_decree.md
│   ├── 03_tax_risk_and_penalty.md
│   ├── 04_sme_credit_guarantee.md
│   └── 05_loan_renewal_document_check.md
└── src/
    ├── __init__.py
    ├── analyzer.py
    ├── data_loader.py
    ├── llm.py
    ├── report.py
    └── retriever.py
```

## How to Run

### 1. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Add your API key

Copy `.env.example` and rename it to `.env`.

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
USE_OPENAI_EMBEDDINGS=false
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

Do not upload `.env` to GitHub.

### 3. Run the application

```bash
python -m streamlit run app.py
```

The app will open at:

```text
http://localhost:8501
```

## Run on Windows

```bash
run_app.bat
```

## Run on Linux or macOS

```bash
bash run_app.sh
```

## Demo Workflow

1. Open the Streamlit app.
2. Select an SME profile from the sidebar.
3. Select a policy document.
4. Review the impact score and risk level.
5. Check the reasons and action checklist.
6. Ask the RAG chatbot questions such as:

```text
Why is this policy high impact for this SME?
What documents should the SME prepare?
Does invoice compliance affect loan renewal?
Summarize this policy in simple words.
```

## Data Notes

The project uses sample SME profiles and short policy knowledge documents. The policy notes are built from public sources and rewritten for demo purposes. They are not official legal text and should not be used as legal, tax, or financial advice.
