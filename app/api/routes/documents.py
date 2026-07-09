from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status

from app.api.dependencies import get_document_service
from app.core.exceptions import DocumentNotFoundError, DocumentProcessingError, FileTooLargeError, UnsupportedFileTypeError
from app.models.responses import ErrorResponse
from app.schemas.document import DocumentListQuery, DocumentUploadResponse
from app.services.document_service import DocumentService

router = APIRouter(tags=["documents"])


@router.post("/upload", response_model=list[DocumentUploadResponse])
async def upload_documents(
    files: list[UploadFile] = File(...),
    document_service: DocumentService = Depends(get_document_service),
) -> list[DocumentUploadResponse]:
    responses: list[DocumentUploadResponse] = []
    for uploaded_file in files:
        try:
            metadata = document_service.upload(uploaded_file)
            responses.append(
                DocumentUploadResponse(
                    document_id=metadata["document_id"],
                    filename=metadata["filename"],
                    status="processed",
                    message="Document uploaded and indexed successfully.",
                    chunk_count=metadata.get("chunk_count", 0),
                )
            )
        except (UnsupportedFileTypeError, FileTooLargeError, DocumentProcessingError) as exc:
            responses.append(
                DocumentUploadResponse(
                    document_id="",
                    filename=uploaded_file.filename or "unknown",
                    status="failed",
                    message=str(exc),
                )
            )
    return responses


@router.get("")
async def list_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    file_type: str | None = None,
    document_service: DocumentService = Depends(get_document_service),
) -> list[dict[str, object]]:
    return document_service.list_documents(page=page, page_size=page_size, search=search, file_type=file_type)


@router.get("/{document_id}")
async def get_document(document_id: str, document_service: DocumentService = Depends(get_document_service)) -> dict[str, object]:
    try:
        return document_service.get_document(document_id)
    except DocumentNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{document_id}")
async def delete_document(document_id: str, document_service: DocumentService = Depends(get_document_service)) -> dict[str, str]:
    try:
        document_service.delete_document(document_id)
        return {"status": "deleted"}
    except DocumentNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/{document_id}/reprocess")
async def reprocess_document(document_id: str, document_service: DocumentService = Depends(get_document_service)) -> dict[str, object]:
    try:
        return document_service.reprocess_document(document_id)
    except DocumentNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
