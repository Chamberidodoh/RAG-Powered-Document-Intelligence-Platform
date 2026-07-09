from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sources: list[dict[str, Any]] = Field(default_factory=list)
    session_id: str


class ChatQueryRequest(BaseModel):
    question: str
    session_id: str | None = None
    document_ids: list[str] = Field(default_factory=list)
    top_k: int | None = None


class ChatQueryResponse(BaseModel):
    answer: str
    session_id: str
    sources: list[dict[str, Any]] = Field(default_factory=list)
    retrieval_time_ms: int
    generation_time_ms: int
