from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

from app.core.config import settings
from app.core.exceptions import DocumentProcessingError, EmptyDocumentError, UnsupportedFileTypeError
from app.loaders import get_loader_for_extension
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from app.utils.file_utils import get_file_extension, get_file_size_bytes, save_uploaded_file, validate_file
from app.utils.id_utils import generate_document_id
from app.utils.text_utils import build_metadata, clean_text, split_text_into_chunks

logger = logging.getLogger(__name__)


class IngestionService:
    def __init__(self, embedding_service: EmbeddingService | None = None, vector_store_service: VectorStoreService | None = None) -> None:
        self.embedding_service = embedding_service or EmbeddingService()
        self.vector_store_service = vector_store_service or VectorStoreService()

    def ingest_file(self, uploaded_file: Any, file_path: Path | None = None) -> dict[str, Any]:
        start = time.perf_counter()
        if not getattr(uploaded_file, "filename", None):
            raise UnsupportedFileTypeError("Missing file name")
        validate_file(uploaded_file.filename)
        file_path = file_path or save_uploaded_file(uploaded_file)
        extension = get_file_extension(uploaded_file.filename)
        loader = get_loader_for_extension(extension)
        text = loader.load(file_path)
        text = clean_text(text)
        if not text.strip():
            raise EmptyDocumentError("Document content is empty")
        chunks = split_text_into_chunks(text, chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)
        if not chunks:
            raise DocumentProcessingError("No chunks were created from the document")
        document_id = generate_document_id()
        records: list[dict[str, Any]] = []
        for index, chunk in enumerate(chunks):
            embedding = self.embedding_service.embed_text(chunk)
            metadata = build_metadata(document_id=document_id, filename=file_path.name, file_type=extension.lstrip("."), page_number=None, chunk_index=index)
            records.append({"id": f"{document_id}-{index}", "content": chunk, "metadata": metadata, "embedding": embedding})
        self.vector_store_service.add_documents(records)
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        logger.info("Document ingested", extra={"document_id": document_id, "chunk_count": len(chunks), "duration_ms": elapsed_ms})
        return {"document_id": document_id, "chunk_count": len(chunks), "file_path": str(file_path), "filename": file_path.name, "file_size_bytes": get_file_size_bytes(file_path)}
