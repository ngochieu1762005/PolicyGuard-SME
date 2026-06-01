import pandas as pd
import streamlit as st

from src.analyzer import ask_bot, get_data, run_check


st.set_page_config(
    page_title="PolicyGuard SME",
    layout="wide"
)

st.markdown(
    """
    <style>
        .block-container {padding-top: 1.6rem;}
        .small-note {color: #64748b; font-size: 14px;}
        .title {font-size: 36px; font-weight: 800; color: #0f172a;}
        .hl {color: #0f766e;}
        .box {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

smes, docs, rules = get_data()

st.markdown('<div class="title">PolicyGuard <span class="hl">SME</span></div>', unsafe_allow_html=True)
st.markdown(
    '<p class="small-note">Demo MVP: đọc chính sách, so với hồ sơ SME, chấm mức ảnh hưởng và gợi ý việc cần làm.</p>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("Chọn dữ liệu demo")

    sme_name = st.selectbox(
        "Hồ sơ doanh nghiệp",
        smes["business_name"].tolist(),
    )

    doc_title = st.selectbox(
        "Văn bản / chính sách",
        docs["title"].tolist(),
    )

    st.divider()
    st.caption(
        "Dữ liệu trong bản này là dữ liệu mẫu để demo hackathon. "
        "Phần chấm điểm dùng rule đơn giản để dễ giải thích với ban giám khảo."
    )

sme = smes.loc[smes["business_name"] == sme_name].iloc[0].to_dict()
doc = docs.loc[docs["title"] == doc_title].iloc[0].to_dict()
res = run_check(sme, doc, rules)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Impact score", f"{res['score']}/100")
m2.metric("Mức ảnh hưởng", res["level"])
m3.metric("Nhóm chính sách", doc["policy_type"])
m4.metric("Giai đoạn vay", sme["loan_stage"])

left, right = st.columns([1.05, 1])

with left:
    st.subheader("1. Hồ sơ SME")
    show_sme = pd.DataFrame(
        [
            ["Tên doanh nghiệp", sme["business_name"]],
            ["Ngành", sme["sector"]],
            ["Quy mô", sme["employee_size"]],
            ["Doanh thu/năm", sme["annual_revenue_vnd"]],
            ["Có khoản vay", sme["has_bank_loan"]],
            ["Giai đoạn vay", sme["loan_stage"]],
            ["Hồ sơ còn thiếu", sme["missing_documents"]],
        ],
        columns=["Thông tin", "Giá trị"],
    )
    st.dataframe(show_sme, use_container_width=True, hide_index=True)

with right:
    st.subheader("2. Tóm tắt chính sách")
    st.markdown(f"**{doc['title']}**")
    st.info(doc["summary"])
    st.write("**Ngày hiệu lực:**", doc["effective_date"])
    st.write("**Từ khóa:**", doc["keywords"])

st.subheader("3. Phân tích tác động")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**Vì sao có mức ảnh hưởng này?**")
    for i, txt in enumerate(res["reasons"], start=1):
        st.write(f"{i}. {txt}")

with col_b:
    st.markdown("**Checklist đề xuất**")
    for txt in res["tasks"]:
        st.checkbox(txt, value=False)

st.subheader("4. Hỏi nhanh trợ lý")
q = st.text_input(
    "Ví dụ: Vì sao ảnh hưởng cao? Tôi cần chuẩn bị giấy tờ gì? Tóm tắt chính sách này giúp tôi."
)

if q.strip():
    st.success(ask_bot(q, sme, doc, res))

with st.expander("Xem toàn bộ văn bản/chính sách mẫu"):
    st.dataframe(
        docs[["policy_id", "title", "policy_type", "effective_date", "source_reference"]],
        use_container_width=True,
        hide_index=True,
    )
