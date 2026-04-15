"""Insights endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.context.builder import build_context
from app.core.inference.reasoning import generate_insights
from app.domain.memory.service import MemoryService
from app.schemas.context import ContextQuery


router = APIRouter(tags=["insights"])
_memory_service = MemoryService()


@router.get("/insights")
def insights(query: ContextQuery = Depends()) -> dict:
    """Return insights for the current user state."""

    memories = _memory_service.get_recent_memories(query.user_id, limit=50, session_id=query.session_id)
    structured = build_context(memories)
    return {"insights": generate_insights(structured)}
