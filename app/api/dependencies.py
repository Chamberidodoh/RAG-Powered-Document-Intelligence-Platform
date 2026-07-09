from fastapi import Depends

from app.services.chat_service import ChatService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.ingestion_service import IngestionService
from app.services.retrieval_service import RetrievalService
from app.services.vector_store_service import VectorStoreService


def get_document_service() -> DocumentService:
    return DocumentService()


def get_ingestion_service() -> IngestionService:
    return IngestionService()


def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()


def get_vector_store_service() -> VectorStoreService:
    return VectorStoreService()


def get_retrieval_service() -> RetrievalService:
    return RetrievalService()


def get_chat_service() -> ChatService:
    return ChatService()
