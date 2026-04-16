"""Chat endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.application.chat_usecase import ChatUseCase
from app.core.response.contracts import success_response
from app.schemas.chat import ChatRequest
from app.domain.memory.service import MemoryService


router = APIRouter(tags=["chat"])
_chat_usecase = ChatUseCase(memory_service=MemoryService())


@router.post("/chat")
async def chat(payload: ChatRequest, user_id: str = Depends(get_current_user)) -> dict:
	"""Process a chat message through Cognet."""

	result = await _chat_usecase.handle_chat_async(
		user_id=user_id,
		message=payload.message,
		session_id=payload.session_id,
	)
	return success_response(result, meta={"endpoint": "chat"})
