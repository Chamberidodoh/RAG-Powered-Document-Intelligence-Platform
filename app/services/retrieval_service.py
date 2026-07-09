from __future__ import annotations

import time
from typing import Any

from app.core.config import settings
from app.core.exceptions import RetrievalError
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService


class RetrievalService:
    def __init__(self, embedding_service: EmbeddingService | None = None, vector_store_service: VectorStoreService | None = None) -> None:
        self.embedding_service = embedding_service or EmbeddingService()
        self.vector_store_service = vector_store_service or VectorStoreService()

    def retrieve(self, question: str, top_k: int | None = None, document_ids: list[str] | None = None) -> tuple[list[dict[str, Any]], int]:
        start = time.perf_counter()
        if not question.strip():
            raise RetrievalError("Question cannot be empty")
        query_embedding = self.embedding_service.embed_text(question)
        results = self.vector_store_service.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k or settings.default_top_k,
            document_ids=document_ids,
        )
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return results, elapsed_ms
