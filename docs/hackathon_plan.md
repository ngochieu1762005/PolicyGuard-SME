# Hackathon Implementation Plan

## Goal after 3 days

A working demo showing:

```text
select SME profile
→ select/upload policy document
→ summarize policy
→ calculate impact score
→ show alert and checklist
→ answer basic questions
```

## Day 1 — Data, scope, and interface

### Goal
Build the foundation for the product demo.

### Tasks

- Define MVP scope: tax, invoice, loan renewal, revenue evidence, cashflow documents.
- Create 3–5 SME demo profiles with different risk levels.
- Prepare 5–10 policy samples.
- Create scoring rules.
- Build basic Streamlit dashboard.
- Define demo script.

### Output

- demo data ready;
- basic UI ready;
- demo flow clear;
- MVP scope fixed.

## Day 2 — AI analysis and impact scoring

### Goal
Build the analysis engine.

### Tasks

- Parse policy text.
- Summarize policy content.
- Extract important information: topic, affected group, required documents, deadlines.
- Match policy with SME profile.
- Calculate impact score.
- Generate reasons and action checklist.
- Add simple chatbot response logic.

### Output

- policy summary;
- impact score;
- alert level;
- checklist;
- chatbot Q&A.

## Day 3 — Integration, demo, and pitch

### Goal
Make the prototype presentable.

### Tasks

- Integrate UI and analysis engine.
- Improve dashboard cards and layout.
- Test 2–3 demo cases: high, medium, low impact.
- Prepare pitch deck.
- Prepare 7-minute demo script.
- Prepare Q&A on data privacy, reliability, and future integration.

### Output

- working prototype;
- clear demo cases;
- complete pitch deck;
- ready-to-present story.

## Post-hackathon roadmap

### 0–3 months

- expand policy documents;
- refine scoring rules by sector;
- improve dashboard and chatbot;
- collect expert feedback.

### 3–6 months

- add official document sources;
- build RAG with vector database;
- evaluate scoring with relationship managers;
- add role-based dashboard.

### 6–12 months

- pilot with selected SME customers;
- integrate with CRM or mobile banking;
- add logging, access control, and security checks;
- track KPIs: time saved, missing document rate, customer satisfaction.
