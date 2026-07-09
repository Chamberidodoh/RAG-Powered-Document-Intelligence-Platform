from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_chat_service
from app.core.exceptions import InvalidQuestionError, OpenAIAPIError
from app.models.chat import ChatQueryRequest, ChatQueryResponse
from app.services.chat_service import ChatService

router = APIRouter(tags=["chat"])


@router.post("/query", response_model=ChatQueryResponse)
async def query_chat(
    payload: ChatQueryRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatQueryResponse:
    try:
        response = chat_service.ask_question(
            question=payload.question,
            session_id=payload.session_id,
            document_ids=payload.document_ids,
            top_k=payload.top_k,
        )
        return ChatQueryResponse(**response)
    except InvalidQuestionError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except OpenAIAPIError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc


@router.delete("/sessions/{session_id}")
async def clear_session(session_id: str, chat_service: ChatService = Depends(get_chat_service)) -> dict[str, str]:
    return {"status": "cleared", "session_id": session_id}
