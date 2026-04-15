from __future__ import annotations

from fastapi import APIRouter

from app.core.embedding.engine import generate_embedding
from app.core.events.event_bus import event_bus
from app.domain.memory.service import MemoryService


router = APIRouter(tags=["webhooks"])
_memory_service = MemoryService()


@router.post("/webhook")
def webhook(data: dict) -> dict:
    """Receive external data and publish it into Cognet."""

    event_bus.publish("webhook_received", data)
    user_id = str(data.get("user_id", "webhook"))
    content = str(data.get("content") or data.get("message") or data)
    memory = _memory_service.save_memory(user_id, content, generate_embedding(content))
    return {"status": "received", "memory": memory}
