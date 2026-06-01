# Data Notes

## Public sources used for context

The project uses public web sources to design the prototype data schema and policy themes:

1. OECD: SME and Entrepreneurship Policy in Viet Nam
2. National Statistics Office of Viet Nam: Statistical Yearbook and enterprise statistics
3. Law on Support for Small- and Medium-sized Enterprises 2017
4. UNU-WIDER: Viet Nam SME database
5. Public SME policy articles and business support policy summaries

See `data/source_references.csv` for the exact URLs included in the project folder.

## Why synthetic data is used

A real banking prototype would require confidential data such as customer profiles, loan status, internal document checklists, transaction history, and relationship manager notes. Those should not be used in a public hackathon folder.

Therefore, this MVP uses:

- synthetic SME profiles;
- public-theme policy records;
- demo internal policy records;
- transparent rule-based scoring.

## Suggested data request for organizers/bank

For a more realistic pilot, the team would request:

| Data type | Purpose | Desired format |
|---|---|---|
| anonymized SME profile data | match policies to SME context | CSV/Excel/API |
| anonymized loan application status | detect renewal/application risk | CSV/Excel/API |
| internal SME document checklist | generate accurate action checklist | Excel/knowledge base |
| policy/regulation documents | RAG and NLP analysis | PDF/Word/TXT |
| expert-labeled impact examples | evaluate scoring accuracy | CSV/Excel |

## Privacy principle

Only minimum necessary and anonymized data should be used. The MVP does not require personal identity data.
