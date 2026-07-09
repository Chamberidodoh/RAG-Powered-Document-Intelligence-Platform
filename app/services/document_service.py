from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from app.core.config import settings
from app.core.exceptions import DocumentNotFoundError, DocumentProcessingError
from app.models.document import DocumentMetadata
from app.services.embedding_service import EmbeddingService
from app.services.ingestion_service import IngestionService
from app.services.vector_store_service import VectorStoreService
from app.utils.file_utils import get_file_extension, get_file_size_bytes
from app.utils.id_utils import generate_document_id

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self, ingestion_service: IngestionService | None = None, vector_store_service: VectorStoreService | None = None) -> None:
        self.ingestion_service = ingestion_service or IngestionService()
        self.vector_store_service = vector_store_service or VectorStoreService()
        self.metadata_dir = Path(settings.metadata_directory)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

    def _metadata_path(self, document_id: str) -> Path:
        return self.metadata_dir / f"{document_id}.json"

    def _store_metadata(self, document_id: str, metadata: dict[str, Any]) -> None:
        self._metadata_path(document_id).write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    def _load_metadata(self, document_id: str) -> dict[str, Any] | None:
        path = self._metadata_path(document_id)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def upload(self, uploaded_file: Any) -> dict[str, Any]:
        result = self.ingestion_service.ingest_file(uploaded_file)
        metadata = {
            "document_id": result["document_id"],
            "filename": result["filename"],
            "file_type": get_file_extension(result["filename"]).lstrip("."),
            "file_size_bytes": result["file_size_bytes"],
            "uploaded_at": __import__("datetime").datetime.utcnow().isoformat(),
            "chunk_count": result["chunk_count"],
            "status": "processed",
            "storage_path": result["file_path"],
        }
        self._store_metadata(result["document_id"], metadata)
        return metadata

    def list_documents(self, page: int = 1, page_size: int = 20, search: str | None = None, file_type: str | None = None) -> list[dict[str, Any]]:
        matches: list[dict[str, Any]] = []
        for path in self.metadata_dir.glob("*.json"):
            metadata = json.loads(path.read_text(encoding="utf-8"))
            if search and search.lower() not in metadata.get("filename", "").lower():
                continue
            if file_type and metadata.get("file_type") != file_type:
                continue
            matches.append(metadata)
        return matches[(page - 1) * page_size : page * page_size]

    def get_document(self, document_id: str) -> dict[str, Any]:
        metadata = self._load_metadata(document_id)
        if not metadata:
            raise DocumentNotFoundError("The requested document could not be found.")
        return metadata

    def delete_document(self, document_id: str) -> None:
        metadata = self._load_metadata(document_id)
        if not metadata:
            raise DocumentNotFoundError("The requested document could not be found.")
        storage_path = Path(metadata.get("storage_path", ""))
        if storage_path.exists():
            storage_path.unlink()
        self._metadata_path(document_id).unlink(missing_ok=True)
        self.vector_store_service.delete_by_document_id(document_id)
        logger.info("Document deleted", extra={"document_id": document_id})

    def reprocess_document(self, document_id: str) -> dict[str, Any]:
        metadata = self._load_metadata(document_id)
        if not metadata:
            raise DocumentNotFoundError("The requested document could not be found.")
        storage_path = Path(metadata.get("storage_path", ""))
        if not storage_path.exists():
            raise DocumentProcessingError("Stored document file no longer exists")
        self.delete_document(document_id)
        # re-upload using a simple mock file object; in a real deployment use the saved file directly
        class _FileLike:
            def __init__(self, name: str, content: bytes) -> None:
                self.filename = name
                self.file = __import__("io").BytesIO(content)

        file_like = _FileLike(storage_path.name, storage_path.read_bytes())
        return self.upload(file_like)
