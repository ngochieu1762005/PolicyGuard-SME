# PolicyGuard SME

Prototype nhỏ cho ý tưởng hackathon: hệ thống hỗ trợ doanh nghiệp nhỏ và ngân hàng theo dõi chính sách mới, đánh giá mức ảnh hưởng đến hồ sơ SME và gợi ý việc cần làm.

## Chạy project

```bash
pip install -r requirements.txt
streamlit run app.py
```

Trên Windows có thể chạy:

```bash
run_app.bat
```

## Project có gì?

- Chọn hồ sơ SME mẫu.
- Chọn văn bản/chính sách mẫu.
- Hệ thống so khớp chính sách với hồ sơ doanh nghiệp.
- Tính Impact Score theo rule dễ giải thích.
- Sinh lý do ảnh hưởng và checklist hành động.
- Có chatbot hỏi đáp đơn giản cho demo.

## Cấu trúc

```text
policyguard_sme_project/
├── app.py
├── data/
│   ├── sme_profiles.csv
│   ├── policies.csv
│   ├── rules.json
│   └── source_references.csv
├── sample_documents/
├── src/
│   └── analyzer.py
└── docs/
```

## Lưu ý

Dữ liệu trong project là dữ liệu mẫu/synthetic để demo. Project chưa dùng dữ liệu ngân hàng thật và không thay thế tư vấn pháp lý hay tư vấn tín dụng chính thức.
