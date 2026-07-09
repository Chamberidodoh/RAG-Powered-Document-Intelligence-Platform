from typing import Any

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    error: dict[str, Any] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
