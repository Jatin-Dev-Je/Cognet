"""Memory endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.embedding.engine import generate_embedding
from app.domain.memory.service import MemoryService
from app.schemas.memory import MemoryCreateRequest


router = APIRouter(tags=["memory"])
_memory_service = MemoryService()


@router.post("/memory/add")
def add_memory(payload: MemoryCreateRequest) -> dict:
	"""Add a memory through the developer API."""

	memory = _memory_service.save_memory(
		payload.user_id,
		payload.content,
		generate_embedding(payload.content),
		session_id=payload.session_id,
		goal=payload.goal,
	)
	return {"status": "saved", "memory": memory}
