"""Memory endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.embedding.engine import generate_embedding
from app.domain.memory.service import MemoryService


router = APIRouter(tags=["memory"])
_memory_service = MemoryService()


@router.post("/memory/add")
def add_memory(payload: dict) -> dict:
	"""Add a memory through the developer API."""

	user_id = payload.get("user_id", "developer")
	content = payload.get("content", "")
	session_id = payload.get("session_id")
	goal = payload.get("goal")
	memory = _memory_service.save_memory(user_id, content, generate_embedding(content), session_id=session_id, goal=goal)
	return {"status": "saved", "memory": memory}
