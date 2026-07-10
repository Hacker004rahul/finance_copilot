from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.rag.hybrid_search import STORE_DIR, embed_text, tokenize


KB_DIR = ROOT / "data" / "kb"
INDEX_PATH = STORE_DIR / "index.json"


def chunk_markdown(text: str, min_chars: int = 500, max_chars: int = 1500) -> list[str]:
    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= max_chars:
            current = candidate
            continue
        if current:
            chunks.append(current)
        if len(paragraph) <= max_chars:
            current = paragraph
            continue
        for start in range(0, len(paragraph), max_chars):
            part = paragraph[start : start + max_chars].strip()
            if part:
                chunks.append(part)
        current = ""

    if current:
        chunks.append(current)

    merged: list[str] = []
    for chunk in chunks:
        if merged and len(chunk) < min_chars and len(merged[-1]) + len(chunk) + 2 <= max_chars:
            merged[-1] = f"{merged[-1]}\n\n{chunk}"
        else:
            merged.append(chunk)
    return merged


def build_index() -> list[dict]:
    records: list[dict] = []
    for path in sorted(KB_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for index, chunk in enumerate(chunk_markdown(text), 1):
            records.append(
                {
                    "id": f"{path.stem}-{index}",
                    "source": path.name,
                    "text": chunk,
                    "tokens": tokenize(chunk),
                    "embedding": embed_text(chunk),
                }
            )
    return records


def main() -> None:
    if not KB_DIR.exists():
        raise SystemExit("Knowledge base not found. Run scripts/generate_synthetic_data.py first.")
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    records = build_index()
    INDEX_PATH.write_text(json.dumps(records, indent=2), encoding="utf-8")
    print(f"Ingested {len(records)} chunks into {INDEX_PATH}")


if __name__ == "__main__":
    main()
