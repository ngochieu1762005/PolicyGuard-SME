import os
import numpy as np
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()


class TfidfRetriever:
    def __init__(self, chunks: list[dict]):
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform([c["text"] for c in chunks])

    def search(self, query: str, top_k: int = 4) -> list[dict]:
        if not query.strip():
            return []
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix).ravel()
        order = np.argsort(scores)[::-1][:top_k]
        results = []
        for i in order:
            item = dict(self.chunks[int(i)])
            item["score"] = float(scores[int(i)])
            results.append(item)
        return results


class OpenAIEmbeddingRetriever:
    def __init__(self, chunks: list[dict]):
        from openai import OpenAI
        self.chunks = chunks
        self.model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.embeddings = self._embed([c["text"] for c in chunks])

    def _embed(self, texts: list[str]) -> np.ndarray:
        response = self.client.embeddings.create(model=self.model, input=texts)
        return np.array([item.embedding for item in response.data], dtype=float)

    def search(self, query: str, top_k: int = 4) -> list[dict]:
        q = self._embed([query])[0]
        denom = np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(q)
        scores = np.dot(self.embeddings, q) / np.maximum(denom, 1e-9)
        order = np.argsort(scores)[::-1][:top_k]
        results = []
        for i in order:
            item = dict(self.chunks[int(i)])
            item["score"] = float(scores[int(i)])
            results.append(item)
        return results


def build_retriever(chunks: list[dict]):
    use_openai = os.getenv("USE_OPENAI_EMBEDDINGS", "false").lower() == "true"
    has_key = bool(os.getenv("OPENAI_API_KEY"))
    if use_openai and has_key:
        return OpenAIEmbeddingRetriever(chunks)
    return TfidfRetriever(chunks)
