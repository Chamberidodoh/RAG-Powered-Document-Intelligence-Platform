from __future__ import annotations

import logging
import time
from typing import Any

from openai import OpenAI

from app.core.config import settings
from app.core.exceptions import InvalidQuestionError, OpenAIAPIError
from app.services.retrieval_service import RetrievalService
from app.utils.id_utils import generate_session_id

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self, retrieval_service: RetrievalService | None = None, client: OpenAI | None = None) -> None:
        self.retrieval_service = retrieval_service or RetrievalService()
        self.client = client

    def ask_question(self, question: str, session_id: str | None = None, document_ids: list[str] | None = None, top_k: int | None = None) -> dict[str, Any]:
        if not question.strip():
            raise InvalidQuestionError("Question cannot be empty")
        session_id = session_id or generate_session_id()
        retrieval_start = time.perf_counter()
        retrieved_chunks, retrieval_time_ms = self.retrieval_service.retrieve(question, top_k=top_k, document_ids=document_ids)
        retrieval_elapsed_ms = int((time.perf_counter() - retrieval_start) * 1000)
        context = "\n\n".join(item["content"] for item in retrieved_chunks)
        prompt = (
            "You are an enterprise document assistant.\n"
            "Answer the user's question using only the supplied document context.\n\n"
            "Rules:\n"
            "1. Do not use outside knowledge.\n"
            "2. Do not invent information.\n"
            "3. If the answer is not present in the context, say: 'I could not find this information in the uploaded documents.'\n"
            "4. Cite the filename and page number for every important claim.\n"
            "5. Provide a concise answer first, followed by supporting details.\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{question}"
        )
        generation_start = time.perf_counter()
        if not settings.openai_api_key:
            answer = f"Local fallback response: {question}"
            generation_elapsed_ms = int((time.perf_counter() - generation_start) * 1000)
        else:
            try:
                client = self.client or OpenAI(api_key=settings.openai_api_key)
                completion = client.responses.create(
                    model=settings.openai_chat_model,
                    input=prompt,
                    temperature=settings.openai_temperature,
                )
                answer = completion.output_text
            except Exception as exc:  # pragma: no cover - defensive
                raise OpenAIAPIError("Failed to generate a response") from exc
            generation_elapsed_ms = int((time.perf_counter() - generation_start) * 1000)
        sources = [
            {
                "filename": item.get("metadata", {}).get("filename"),
                "page_number": item.get("metadata", {}).get("page_number"),
                "chunk_index": item.get("metadata", {}).get("chunk_index"),
                "excerpt": item.get("content"),
                "similarity_score": item.get("distance"),
            }
            for item in retrieved_chunks
        ]
        return {
            "answer": answer,
            "session_id": session_id,
            "sources": sources,
            "retrieval_time_ms": retrieval_time_ms,
            "generation_time_ms": generation_elapsed_ms,
        }
