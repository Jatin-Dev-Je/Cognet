"""Memory endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.core.ai.embedding import generate_embedding_async
from app.core.response.contracts import success_response
from app.domain.memory.service import MemoryService
from app.schemas.memory import MemoryCreateRequest


router = APIRouter(tags=["memory"])
_memory_service = MemoryService()


@router.post("/memory/add")
async def add_memory(payload: MemoryCreateRequest, user_id: str = Depends(get_current_user)) -> dict:
	"""Add a memory through the developer API."""

	resolved_user_id = payload.user_id or user_id
	memory = await _memory_service.save_memory_async(
		resolved_user_id,
		payload.content,
		await generate_embedding_async(payload.content),
		session_id=payload.session_id,
		goal=payload.goal,
	)
	return success_response({"status": "saved", "memory": memory}, meta={"endpoint": "memory_add"})
