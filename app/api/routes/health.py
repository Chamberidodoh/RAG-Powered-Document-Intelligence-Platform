from fastapi import APIRouter

from app.models.responses import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        service="rag-document-intelligence-api",
        version="1.0.0",
    )
