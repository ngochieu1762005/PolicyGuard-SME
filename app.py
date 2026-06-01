from pathlib import Path
import pandas as pd
import streamlit as st

from src.data_loader import read_csv, read_documents, make_chunks
from src.retriever import build_retriever
from src.analyzer import load_rules, analyze_policy
from src.llm import ask_openai, has_openai_key
from src.report import make_markdown_report

st.set_page_config(
    page_title="PolicyGuard SME",
    page_icon="PG",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
:root {
    --blue: #2563eb;
    --ink: #0f172a;
    --muted: #64748b;
    --line: #e2e8f0;
    --bg: #ffffff;
    --soft: #f8fafc;
}
.block-container { padding-top: 1.4rem; max-width: 1240px; }
.stApp { background: #ffffff; color: var(--ink); }
.hero {
    border: 1px solid var(--line);
    border-radius: 26px;
    padding: 30px 34px;
    background: linear-gradient(135deg, #ffffff 0%, #f8fbff 52%, #eff6ff 100%);
    box-shadow: 0 18px 48px rgba(15, 23, 42, 0.07);
    margin-bottom: 22px;
}
.hero h1 { margin: 0; font-size: 42px; letter-spacing: -1.2px; }
.hero p { color: var(--muted); font-size: 17px; max-width: 850px; line-height: 1.65; }
.badge {
    display: inline-block;
    border: 1px solid #bfdbfe;
    background: #eff6ff;
    color: #1d4ed8;
    padding: 6px 12px;
    border-radius: 999px;
    font-weight: 650;
    font-size: 13px;
    margin-bottom: 14px;
}
.card {
    border: 1px solid var(--line);
    border-radius: 22px;
    padding: 22px;
    background: var(--bg);
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.055);
    min-height: 130px;
}
.card h3 { margin-top: 0; margin-bottom: 8px; font-size: 17px; }
.card p { color: var(--muted); margin-bottom: 0; line-height: 1.55; }
.metric-card {
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 18px 20px;
    background: #ffffff;
}
.metric-label { color: var(--muted); font-size: 13px; font-weight: 650; }
.metric-value { font-size: 31px; font-weight: 800; letter-spacing: -0.5px; margin-top: 4px; }
.level-high { color: #dc2626; }
.level-medium { color: #d97706; }
.level-low { color: #16a34a; }
.source-box {
    border-left: 4px solid #2563eb;
    background: #f8fafc;
    padding: 14px 16px;
    border-radius: 12px;
    margin-bottom: 10px;
    color: #334155;
}
.small-muted { color: #64748b; font-size: 13px; }
hr { border: none; border-top: 1px solid var(--line); margin: 1.3rem 0; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


@st.cache_data
def get_data():
    smes = read_csv("sme_profiles.csv")
    sources = read_csv("sources.csv")
    docs = read_documents()
    chunks = make_chunks(docs)
    return smes, sources, docs, chunks


@st.cache_resource
def get_retriever(chunks):
    return build_retriever(chunks)


smes, sources_df, docs, chunks = get_data()
retriever = get_retriever(chunks)
rules = load_rules()

st.markdown(
    """
    <div class="hero">
        <div class="badge">AI Policy Impact Assistant for SMEs</div>
        <h1>PolicyGuard SME</h1>
        <p>
        A modern RAG-based demo that helps small and medium-sized enterprises understand how policy,
        tax, invoice, and banking-related requirements may affect loan renewal, compliance documents,
        and next actions.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("Setup")
    if has_openai_key():
        st.success("OpenAI API key detected")
    else:
        st.warning("No OpenAI API key found. Chat will use local fallback.")

    selected_sme_name = st.selectbox("Choose SME profile", smes["business_name"].tolist())
    selected_doc_title = st.selectbox("Choose policy document", [d["title"] for d in docs])

    st.markdown("---")
    st.caption("Optional: paste a new policy text for analysis")
    custom_policy = st.text_area("Custom policy text", height=180, placeholder="Paste a policy or requirement here...")

sme_row = smes[smes["business_name"] == selected_sme_name].iloc[0]
sme = sme_row.to_dict()
selected_doc = next(d for d in docs if d["title"] == selected_doc_title)
policy_text = custom_policy.strip() if custom_policy.strip() else selected_doc["text"]
policy_title = "Custom pasted policy" if custom_policy.strip() else selected_doc["title"]

query_for_retrieval = (
    f"{policy_title}\n{policy_text[:1200]}\nSME sector {sme.get('sector')} loan {sme.get('loan_stage')} "
    f"missing documents {sme.get('missing_documents')}"
)
retrieved = retriever.search(query_for_retrieval, top_k=5)
analysis = analyze_policy(policy_text + "\n" + "\n".join([r["text"] for r in retrieved[:2]]), sme, rules)

left, right = st.columns([1.05, 1])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Selected SME")
    c1, c2, c3 = st.columns(3)
    c1.metric("Sector", sme.get("sector"))
    c2.metric("Employees", int(sme.get("employees")))
    c3.metric("Loan", sme.get("has_bank_loan"))
    st.write(f"**Business name:** {sme.get('business_name')}")
    st.write(f"**Province:** {sme.get('province')}")
    st.write(f"**Loan stage:** {sme.get('loan_stage')}")
    st.write(f"**Missing documents:** {sme.get('missing_documents')}")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Selected Policy")
    st.write(f"**Policy:** {policy_title}")
    st.write(policy_text[:720] + ("..." if len(policy_text) > 720 else ""))
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### Impact Analysis")
metric_cols = st.columns(4)
level_class = "level-high" if analysis["level"] == "High" else "level-medium" if analysis["level"] == "Medium" else "level-low"
metric_cols[0].markdown(f'<div class="metric-card"><div class="metric-label">Impact Level</div><div class="metric-value {level_class}">{analysis["level"]}</div></div>', unsafe_allow_html=True)
metric_cols[1].markdown(f'<div class="metric-card"><div class="metric-label">Impact Score</div><div class="metric-value">{analysis["score"]}/100</div></div>', unsafe_allow_html=True)
metric_cols[2].markdown(f'<div class="metric-card"><div class="metric-label">Matched Topics</div><div class="metric-value">{len(analysis["topics"])}</div></div>', unsafe_allow_html=True)
metric_cols[3].markdown(f'<div class="metric-card"><div class="metric-label">Actions</div><div class="metric-value">{len(analysis["checklist"])}</div></div>', unsafe_allow_html=True)

st.progress(analysis["score"] / 100)

r1, r2 = st.columns([1, 1])
with r1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Why this result?")
    for reason in analysis["reasons"]:
        st.write(f"- {reason}")
    st.markdown('</div>', unsafe_allow_html=True)

with r2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Action Checklist")
    for item in analysis["checklist"]:
        st.checkbox(item, value=False)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### RAG Chatbot")
chat_left, chat_right = st.columns([1.1, 0.9])
with chat_left:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input("Ask about the policy impact, required documents, or next steps...")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
        query = f"{question}\n{sme}\n{policy_text[:1000]}"
        chat_sources = retriever.search(query, top_k=4)
        answer = ask_openai(question, chat_sources, analysis, sme)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)

with chat_right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Retrieved Sources")
    for item in retrieved:
        st.markdown(
            f"""
            <div class="source-box">
                <b>{item['title']}</b><br>
                <span class="small-muted">{item['chunk_id']} | similarity {item['score']:.3f}</span><br>
                {item['text'][:260]}...
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### Export")
report = make_markdown_report(sme, policy_title, analysis, retrieved)
st.download_button(
    "Download impact report (.md)",
    data=report,
    file_name="policyguard_sme_impact_report.md",
    mime="text/markdown",
)

with st.expander("Public source references used to build the demo dataset"):
    st.dataframe(sources_df, use_container_width=True)

st.caption("Demo only. This application does not replace legal, tax, or financial advice.")
