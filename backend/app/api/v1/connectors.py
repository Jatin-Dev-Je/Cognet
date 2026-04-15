"""Connector endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.events.event_bus import event_bus
from app.domain.connectors.github_connector import GitHubConnector
from app.domain.memory.service import MemoryService
from app.core.embedding.engine import generate_embedding


router = APIRouter(prefix="/connectors", tags=["connectors"])
_memory_service = MemoryService()
_github_connector = GitHubConnector()


@router.post("/github/sync")
def sync_github(user_id: str = "github") -> dict:
    """Fetch mock GitHub activity and store it as memory."""

    raw_data = _github_connector.fetch_data()
    processed_data = _github_connector.process(raw_data)
    saved_memories = []

    for item in processed_data:
        content = item["content"]
        memory = _memory_service.save_memory(user_id, content, generate_embedding(content))
        saved_memories.append(memory)

    event_bus.publish("connector_synced", {"connector": "github", "count": len(saved_memories)})
    return {"status": "synced", "items": processed_data, "saved": saved_memories}
