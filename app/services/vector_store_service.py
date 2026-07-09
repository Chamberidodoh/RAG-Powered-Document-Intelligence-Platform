from __future__ import annotations

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
            normalized_documents = []
            for item in documents:
                metadata = item["metadata"]
                page_number = metadata.get("page_number")
                if page_number is None:
                    page_number = 0
                elif not isinstance(page_number, (int, float)):
                    page_number = 0

                chunk_index = metadata.get("chunk_index", 0)
                if not isinstance(chunk_index, int):
                    chunk_index = 0

                normalized_metadata = {
                    "document_id": str(metadata.get("document_id", "")),
                    "filename": str(metadata.get("filename", "")),
                    "file_type": str(metadata.get("file_type", "")),
                    "page_number": int(page_number),
                    "chunk_index": chunk_index,
                }
                normalized_documents.append({
                    "id": str(item["id"]),
                    "content": str(item["content"]),
                    "metadata": normalized_metadata,
                    "embedding": item.get("embedding"),
                })
            self.collection.add(
                documents=[item["content"] for item in normalized_documents],
                metadatas=[item["metadata"] for item in normalized_documents],
                ids=[item["id"] for item in normalized_documents],
                embeddings=[item.get("embedding") for item in normalized_documents],
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
            if not result:
                return []

            ids = (result.get("ids") or [[]])[0] if result.get("ids") else []
            documents = (result.get("documents") or [[]])[0] if result.get("documents") else []
            metadatas = (result.get("metadatas") or [[]])[0] if result.get("metadatas") else []
            distances = (result.get("distances") or [[]])[0] if result.get("distances") else []

            if not ids:
                return []

            return [
                {
                    "id": id_value,
                    "content": content,
                    "metadata": metadata,
                    "distance": distance,
                }
                for id_value, content, metadata, distance in zip(ids, documents, metadatas, distances)
            ]
        except Exception as exc:  # pragma: no cover - defensive
            raise VectorDatabaseError("Failed to query vector database") from exc
