import os
from dotenv import load_dotenv

load_dotenv()


def has_openai_key() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def format_context(chunks: list[dict]) -> str:
    parts = []
    for i, c in enumerate(chunks, start=1):
        parts.append(
            f"[Source {i}: {c['title']} | {c['chunk_id']} | score={c.get('score', 0):.3f}]\n{c['text']}"
        )
    return "\n\n".join(parts)


def local_answer(question: str, chunks: list[dict], analysis: dict, sme: dict) -> str:
    context = chunks[0]["text"] if chunks else "No context found."
    actions = analysis.get("checklist", [])[:5]
    action_text = "\n".join([f"- {a}" for a in actions]) or "- No specific action found."
    return (
        "I found the most relevant policy context, but no OpenAI API key is configured.\n\n"
        f"Most relevant context:\n{context[:900]}\n\n"
        f"Current impact level for {sme.get('business_name', 'this SME')}: {analysis.get('level')} "
        f"({analysis.get('score')}/100).\n\n"
        f"Suggested actions:\n{action_text}\n\n"
        "To enable a stronger RAG answer, add OPENAI_API_KEY to your .env file."
    )


def ask_openai(question: str, chunks: list[dict], analysis: dict, sme: dict) -> str:
    if not has_openai_key():
        return local_answer(question, chunks, analysis, sme)

    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    context = format_context(chunks)

    prompt = f"""
You are PolicyGuard SME, a banking policy assistant for small and medium-sized enterprises.
Use ONLY the retrieved context, the SME profile, and the impact analysis below.
If the answer is not supported by the context, say that the available information is not sufficient.
Do not provide official legal, tax, or financial advice.

SME profile:
{sme}

Impact analysis:
{analysis}

Retrieved policy context:
{context}

User question:
{question}

Answer in clear, practical English. Include short bullet points when useful.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You answer questions using retrieved policy context for SMEs."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.25,
    )
    return response.choices[0].message.content
