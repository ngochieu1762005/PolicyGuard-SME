from pathlib import Path
import re
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DOC_DIR = BASE_DIR / "documents"


def read_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / name)


def read_documents() -> list[dict]:
    docs = []
    for path in sorted(DOC_DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        meta = {}
        body = raw
        if raw.startswith("---"):
            parts = raw.split("---", 2)
            if len(parts) == 3:
                for line in parts[1].strip().splitlines():
                    if ":" in line:
                        key, value = line.split(":", 1)
                        meta[key.strip()] = value.strip()
                body = parts[2].strip()
        docs.append({
            "file": path.name,
            "id": meta.get("id", path.stem),
            "title": meta.get("title", path.stem.replace("_", " ").title()),
            "topic": meta.get("topic", "general"),
            "source_id": meta.get("source_id", "unknown"),
            "text": body,
        })
    return docs


def make_chunks(docs: list[dict], chunk_size: int = 850, overlap: int = 120) -> list[dict]:
    chunks = []
    for doc in docs:
        text = re.sub(r"\s+", " ", doc["text"]).strip()
        if not text:
            continue
        start = 0
        idx = 1
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()
            chunks.append({
                "chunk_id": f"{doc['id']}-{idx}",
                "doc_id": doc["id"],
                "title": doc["title"],
                "topic": doc["topic"],
                "source_id": doc["source_id"],
                "text": chunk_text,
            })
            if end == len(text):
                break
            start = max(0, end - overlap)
            idx += 1
    return chunks
