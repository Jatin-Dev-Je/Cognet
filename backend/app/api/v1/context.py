"""Context endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.context.builder import build_context, format_context
from app.domain.memory.service import MemoryService


router = APIRouter(tags=["context"])
_memory_service = MemoryService()


@router.get("/context")
def context(user_id: str = "developer", session_id: str | None = None) -> dict:
	"""Return current structured context."""

	memories = _memory_service.get_recent_memories(user_id, limit=50, session_id=session_id)
	structured = build_context(memories)
	return {"context": structured, "formatted_context": format_context(structured)}
