import json
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"


def get_data():
    smes = pd.read_csv(DATA / "sme_profiles.csv")
    docs = pd.read_csv(DATA / "policies.csv")

    with open(DATA / "rules.json", "r", encoding="utf-8") as f:
        rules = json.load(f)

    return smes, docs, rules


def cut_list(text):
    if pd.isna(text):
        return []

    text = str(text).replace(",", ";")
    return [x.strip().lower() for x in text.split(";") if x.strip()]


def level(score):
    if score >= 70:
        return "Cao"
    if score >= 40:
        return "Trung bình"
    return "Thấp"


def has_any(text, words):
    text = text.lower()
    return any(w in text for w in words)


def add_task(tasks, text):
    if text not in tasks:
        tasks.append(text)


def run_check(sme, doc, rules=None):
    sector = str(sme.get("sector", "")).lower()
    tags = cut_list(doc.get("sector_tags", ""))
    miss = cut_list(sme.get("missing_documents", ""))
    doc_type = str(doc.get("policy_type", "")).lower()

    full_text = " ".join(
        [
            str(doc.get("title", "")),
            str(doc.get("summary", "")),
            str(doc.get("keywords", "")),
            doc_type,
        ]
    ).lower()

    score = 0
    why = []
    tasks = []

    if "all" in tags:
        score += 10
        why.append("Chính sách có phạm vi áp dụng rộng cho nhiều nhóm SME.")

    if sector and sector in tags:
        score += 20
        why.append("Ngành của doanh nghiệp nằm trong nhóm bị ảnh hưởng.")

    has_loan = str(sme.get("has_bank_loan", "")).lower() == "yes"
    if has_loan and has_any(doc_type, ["credit", "tax", "compliance"]):
        score += 15
        why.append("Doanh nghiệp đang có khoản vay nên thay đổi chính sách có thể ảnh hưởng đến rà soát hồ sơ.")

    renew = str(sme.get("loan_stage", "")).lower() == "renewal"
    if renew and has_any(full_text, ["renewal", "cashflow", "revenue", "loan"]):
        score += 25
        why.append("Doanh nghiệp đang ở giai đoạn gia hạn vay, trong khi văn bản có nhắc đến hồ sơ/dòng tiền/doanh thu.")
        add_task(tasks, "Chuẩn bị bộ hồ sơ gia hạn vay và xác nhận thời hạn với nhân viên ngân hàng.")

    if any(item in full_text for item in miss):
        score += 25
        why.append("Một số giấy tờ văn bản yêu cầu đang nằm trong nhóm hồ sơ còn thiếu của doanh nghiệp.")

    cash = str(sme.get("cashflow_status", "")).lower()
    if cash in ["unstable", "seasonal"] and "cashflow" in full_text:
        score += 15
        why.append("Dòng tiền của doanh nghiệp chưa ổn định, trong khi chính sách yêu cầu bằng chứng dòng tiền.")
        add_task(tasks, "Tổng hợp sao kê và báo cáo dòng tiền 6 tháng gần nhất.")

    tax = str(sme.get("tax_compliance_status", "")).lower()
    if tax in ["low", "medium"] and has_any(full_text, ["tax", "invoice"]):
        score += 15
        why.append("Mức sẵn sàng về thuế/hóa đơn chưa cao nên cần kiểm tra lại trước khi nộp hồ sơ.")
        add_task(tasks, "Rà soát tờ khai thuế, hóa đơn và chứng từ doanh thu.")

    inv = str(sme.get("digital_invoice_status", "")).lower()
    if inv in ["partial", "not_ready"] and "invoice" in full_text:
        score += 15
        why.append("Dữ liệu hóa đơn điện tử chưa hoàn chỉnh.")
        add_task(tasks, "Xuất và kiểm tra dữ liệu hóa đơn điện tử trong kỳ gần nhất.")

    if "revenue" in full_text:
        add_task(tasks, "Chuẩn bị bằng chứng doanh thu: hợp đồng, hóa đơn, POS export hoặc sao kê ngân hàng.")
    if "tax" in full_text:
        add_task(tasks, "Kiểm tra trạng thái nộp thuế và các khoản còn thiếu nếu có.")
    if "business plan" in full_text:
        add_task(tasks, "Cập nhật kế hoạch kinh doanh và mục đích sử dụng vốn.")
    if "environment" in full_text:
        add_task(tasks, "Chuẩn bị giấy tờ liên quan đến vận hành/môi trường nếu ngành nghề yêu cầu.")

    if not why:
        why.append("Chưa thấy liên hệ mạnh giữa chính sách này và hồ sơ doanh nghiệp. Theo dõi là đủ ở giai đoạn hiện tại.")

    if not tasks:
        tasks.append("Theo dõi chính sách và hỏi nhân viên quan hệ khách hàng nếu có yêu cầu hồ sơ mới.")

    score = min(score, 100)

    return {
        "score": score,
        "level": level(score),
        "reasons": why,
        "tasks": tasks,
        "summary": doc.get("summary", ""),
    }


def ask_bot(q, sme, doc, res):
    q = q.lower().strip()

    if has_any(q, ["vì sao", "tại sao", "why", "lý do", "anh huong", "ảnh hưởng"]):
        return "Mức ảnh hưởng được tính dựa trên: " + "; ".join(res["reasons"])

    if has_any(q, ["chuẩn bị", "giấy tờ", "document", "need", "cần làm"]):
        return "Các việc nên làm: " + "; ".join(res["tasks"])

    if has_any(q, ["tóm tắt", "summary", "nội dung", "noi dung"]):
        return "Tóm tắt: " + str(res["summary"])

    return (
        f"Với hồ sơ của {sme.get('business_name')}, chính sách này đang được đánh giá ở mức "
        f"{res['level']} với điểm {res['score']}/100. Việc nên ưu tiên: {res['tasks'][0]}"
    )
