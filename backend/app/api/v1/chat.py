"""Chat endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from app.application.chat_usecase import ChatUseCase
from app.domain.memory.service import MemoryService


router = APIRouter(tags=["chat"])
_chat_usecase = ChatUseCase(memory_service=MemoryService())


@router.post("/chat")
def chat(payload: dict) -> dict:
	"""Process a chat message through Cognet."""

	return _chat_usecase.handle_chat(
		user_id=payload.get("user_id", "developer"),
		message=payload.get("message", ""),
		session_id=payload.get("session_id"),
	)
