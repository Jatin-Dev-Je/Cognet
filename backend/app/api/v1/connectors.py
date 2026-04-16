"""Connector endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.core.embedding.engine import generate_embedding
from app.core.events.event_bus import event_bus
from app.domain.connectors.github_connector import GitHubConnector
from app.domain.memory.service import MemoryService


router = APIRouter(prefix="/connectors", tags=["connectors"])
_memory_service = MemoryService()
_github_connector = GitHubConnector()


@router.post("/github/sync")
def sync_github(repo: str = "microsoft/vscode", user_id: str = Depends(get_current_user)) -> dict:
    """Fetch public GitHub commits and store them as memory."""

    commits = _github_connector.fetch_commits(repo)
    processed_data = _github_connector.process(commits)
    saved_memories = []

    for item in processed_data:
        content = item["content"]
        memory = _memory_service.save_memory(user_id, content, generate_embedding(content))
        saved_memories.append(memory)

    event_bus.publish("connector_synced", {"connector": "github", "repo": repo, "count": len(saved_memories)})
    return {"status": "synced", "items": processed_data, "saved": saved_memories}
