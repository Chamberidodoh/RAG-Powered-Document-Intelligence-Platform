import re
from typing import Any


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()


def split_text_into_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    if not text:
        return []
    words = text.split()
    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end == len(words):
            break
        start = max(0, end - chunk_overlap)
    return chunks


def build_metadata(document_id: str, filename: str, file_type: str, page_number: int | None = None, chunk_index: int = 0) -> dict[str, Any]:
    return {
        "document_id": document_id,
        "filename": filename,
        "file_type": file_type,
        "page_number": page_number,
        "chunk_index": chunk_index,
    }
