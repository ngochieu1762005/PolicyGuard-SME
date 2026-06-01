import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


def load_rules() -> dict:
    return json.loads((BASE_DIR / "data" / "rules.json").read_text(encoding="utf-8"))


def text_has_any(text: str, words: list[str]) -> bool:
    low = text.lower()
    return any(w.lower() in low for w in words)


def split_items(value) -> list[str]:
    if value is None:
        return []
    return [x.strip() for x in str(value).split(";") if x.strip()]


def analyze_policy(policy_text: str, sme: dict, rules: dict) -> dict:
    score = 0
    matched_topics = []
    required_docs = []
    reasons = []

    for topic, rule in rules.items():
        if text_has_any(policy_text, rule.get("keywords", [])):
            matched_topics.append(topic)
            score += int(rule.get("base_score", 0))
            required_docs.extend(rule.get("documents", []))
            reasons.append(f"The policy contains terms related to {topic.replace('_', ' ')}.")

    if str(sme.get("has_bank_loan", "")).lower() == "yes" and "loan" in matched_topics:
        score += 25
        reasons.append("The SME has an active bank loan, so loan-related requirements are more relevant.")

    loan_stage = str(sme.get("loan_stage", "")).lower()
    if "renewal" in loan_stage and "loan" in matched_topics:
        score += 20
        reasons.append("The SME has an upcoming loan renewal, which increases urgency.")

    missing = split_items(sme.get("missing_documents", ""))
    if missing:
        missing_low = "; ".join(missing).lower()
        hits = [doc for doc in required_docs if doc.lower() in missing_low]
        if hits:
            score += 15
            reasons.append("Some documents required by the policy are currently missing in the SME profile.")

    score = min(score, 100)
    if score >= 70:
        level = "High"
    elif score >= 40:
        level = "Medium"
    else:
        level = "Low"

    checklist = []
    for item in required_docs:
        clean = item.strip()
        if clean and clean not in checklist:
            checklist.append(clean)

    if "loan" in matched_topics:
        checklist.append("Contact the bank relationship manager before the loan deadline")
    if "tax" in matched_topics:
        checklist.append("Review tax payment status and keep payment proof")
    if "invoice" in matched_topics:
        checklist.append("Organize e-invoice records and sales invoice summaries")

    final_checklist = []
    for item in checklist:
        if item not in final_checklist:
            final_checklist.append(item)

    if not reasons:
        reasons.append("No strong match was found between this policy and the SME profile.")

    return {
        "score": score,
        "level": level,
        "topics": matched_topics,
        "reasons": reasons,
        "checklist": final_checklist[:8],
    }
