from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import chromadb
from chromadb.api.models.Collection import Collection

from app.core.config import settings
from app.core.exceptions import VectorDatabaseError


class VectorStoreService:
    def __init__(self, persist_directory: str | None = None) -> None:
        self.persist_directory = persist_directory or settings.chroma_persist_directory
        self.collection_name = settings.chroma_collection_name
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self._get_or_create_collection()

    def _get_or_create_collection(self) -> Collection:
        try:
            return self.client.get_or_create_collection(self.collection_name)
        except Exception as exc:  # pragma: no cover - defensive
            raise VectorDatabaseError("Failed to initialize vector store") from exc

    def add_documents(self, documents: list[dict[str, Any]]) -> None:
        if not documents:
            return
        try:
            self.collection.add(
                documents=[item["content"] for item in documents],
                metadatas=[item["metadata"] for item in documents],
                ids=[item["id"] for item in documents],
                embeddings=[item.get("embedding") for item in documents],
            )
        except Exception as exc:  # pragma: no cover - defensive
            raise VectorDatabaseError("Failed to store documents in vector database") from exc

    def delete_by_document_id(self, document_id: str) -> None:
        try:
            self.collection.delete(where={"document_id": document_id})
        except Exception as exc:  # pragma: no cover - defensive
            raise VectorDatabaseError("Failed to delete document from vector database") from exc

    def similarity_search(self, query_embedding: list[float], top_k: int = 5, document_ids: list[str] | None = None) -> list[dict[str, Any]]:
        where = {"document_id": {"$in": document_ids}} if document_ids else None
        try:
            result = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where,
            )
            return [
                {
                    "id": ids,
                    "content": content,
                    "metadata": metadata,
                    "distance": distance,
                }
                for ids, content, metadata, distance in zip(
                    result.get("ids", [[]])[0],
                    result.get("documents", [[]])[0],
                    result.get("metadatas", [[]])[0],
                    result.get("distances", [[]])[0],
                )
            ]
        except Exception as exc:  # pragma: no cover - defensive
            raise VectorDatabaseError("Failed to query vector database") from exc
