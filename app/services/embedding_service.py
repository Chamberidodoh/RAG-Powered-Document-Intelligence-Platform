from __future__ import annotations

from openai import OpenAI

from app.core.config import settings
from app.core.exceptions import EmbeddingGenerationError


class EmbeddingService:
    def __init__(self, client: OpenAI | None = None) -> None:
        self.client = client or OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_embedding_model

    def embed_text(self, text: str) -> list[float]:
        try:
            response = self.client.embeddings.create(model=self.model, input=text)
            return response.data[0].embedding
        except Exception as exc:  # pragma: no cover - defensive
            raise EmbeddingGenerationError("Failed to generate embeddings") from exc
