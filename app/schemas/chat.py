from pydantic import BaseModel, Field


class ChatQueryRequestSchema(BaseModel):
    question: str = Field(min_length=1)
    session_id: str | None = None
    document_ids: list[str] = Field(default_factory=list)
    top_k: int | None = None
