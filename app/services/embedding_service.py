from __future__ import annotations

import hashlib
import math

from openai import OpenAI

from app.core.config import settings
from app.core.exceptions import EmbeddingGenerationError


class EmbeddingService:
    def __init__(self, client: OpenAI | None = None) -> None:
        self.client = client
        self.model = settings.openai_embedding_model

    def embed_text(self, text: str) -> list[float]:
        if not settings.openai_api_key:
            return self._local_embedding(text)
        if self.client is None:
            self.client = OpenAI(api_key=settings.openai_api_key)
        try:
            response = self.client.embeddings.create(model=self.model, input=text)
            return response.data[0].embedding
        except Exception as exc:  # pragma: no cover - defensive
            raise EmbeddingGenerationError("Failed to generate embeddings") from exc

    def _local_embedding(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        values = []
        for index in range(8):
            chunk = digest[index : index + 2]
            value = int(chunk, 16) / 255.0
            values.append(round(value + math.sin(index + 1) * 0.1, 6))
        return values
