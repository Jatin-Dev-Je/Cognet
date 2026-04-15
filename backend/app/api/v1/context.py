"""Context endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.context.builder import build_context, format_context
from app.domain.memory.service import MemoryService
from app.schemas.context import ContextQuery


router = APIRouter(tags=["context"])
_memory_service = MemoryService()


@router.get("/context")
def context(query: ContextQuery = Depends()) -> dict:
	"""Return current structured context."""

	memories = _memory_service.get_recent_memories(query.user_id, limit=50, session_id=query.session_id)
	structured = build_context(memories)
	return {"context": structured, "formatted_context": format_context(structured)}
