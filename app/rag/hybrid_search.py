from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

from app.schemas.data_models import SourceChunk


STORE_DIR = Path(__file__).resolve().parent / "store"
INDEX_PATH = STORE_DIR / "index.json"
TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")
VECTOR_SIZE = 384


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_RE.finditer(text)]


def embed_text(text: str) -> list[float]:
    vector = [0.0] * VECTOR_SIZE
    for token, count in Counter(tokenize(text)).items():
        index = hash(token) % VECTOR_SIZE
        vector[index] += 1.0 + math.log(count)
    norm = math.sqrt(sum(value * value for value in vector))
    if norm:
        vector = [value / norm for value in vector]
    return vector


def cosine_similarity(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def keyword_score(query_tokens: set[str], chunk_tokens: list[str]) -> float:
    if not query_tokens or not chunk_tokens:
        return 0.0
    chunk_counts = Counter(chunk_tokens)
    overlap = sum(min(chunk_counts[token], 3) for token in query_tokens)
    return overlap / (len(query_tokens) + 2)


def load_index(index_path: Path = INDEX_PATH) -> list[dict]:
    if not index_path.exists():
        raise FileNotFoundError(
            f"RAG index not found at {index_path}. Run: uv run python scripts/ingest.py"
        )
    return json.loads(index_path.read_text(encoding="utf-8"))


def hybrid_search(query: str, top_k: int = 5, index_path: Path = INDEX_PATH) -> list[SourceChunk]:
    chunks = load_index(index_path)
    query_vector = embed_text(query)
    query_tokens = set(tokenize(query))
    ranked = []

    for chunk in chunks:
        semantic = cosine_similarity(query_vector, chunk["embedding"])
        keyword = keyword_score(query_tokens, chunk["tokens"])
        score = (0.68 * semantic) + (0.32 * keyword)
        ranked.append(
            SourceChunk(source=chunk["source"], text=chunk["text"], score=round(score, 4))
        )

    ranked.sort(key=lambda item: item.score, reverse=True)
    return ranked[:top_k]
