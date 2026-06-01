from datetime import datetime


def make_markdown_report(sme: dict, policy_title: str, analysis: dict, sources: list[dict]) -> str:
    lines = []
    lines.append("# PolicyGuard SME Impact Report")
    lines.append("")
    lines.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    lines.append("## SME Profile")
    for key, value in sme.items():
        lines.append(f"- **{key}**: {value}")
    lines.append("")
    lines.append("## Policy")
    lines.append(f"- **Selected policy**: {policy_title}")
    lines.append("")
    lines.append("## Impact Result")
    lines.append(f"- **Impact level**: {analysis.get('level')}")
    lines.append(f"- **Impact score**: {analysis.get('score')}/100")
    lines.append(f"- **Matched topics**: {', '.join(analysis.get('topics', [])) or 'None'}")
    lines.append("")
    lines.append("## Reasons")
    for r in analysis.get("reasons", []):
        lines.append(f"- {r}")
    lines.append("")
    lines.append("## Recommended Action Checklist")
    for item in analysis.get("checklist", []):
        lines.append(f"- [ ] {item}")
    lines.append("")
    lines.append("## Retrieved Sources")
    for s in sources:
        lines.append(f"- {s.get('title')} ({s.get('chunk_id')})")
    lines.append("")
    lines.append("## Disclaimer")
    lines.append("This report is generated for demo purposes and does not replace legal, tax, or financial advice.")
    return "\n".join(lines)
