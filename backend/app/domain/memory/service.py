"""Memory service for Cognet.

Purpose:
Save memories with classification and timestamps.

Steps:
- classify text
- store content
- store embedding
- store type
- store created_at
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterable

from app.core.inference.classifier import classify_memory


MemoryRecord = dict[str, Any]
_MEMORY_STORE: list[MemoryRecord] = []


def _build_memory_record(user_id: str, content: str, embedding: Iterable[float]) -> MemoryRecord:
	"""Build a memory record with classification and timestamps."""

	return {
		"user_id": user_id,
		"content": content,
		"embedding": list(embedding),
		"type": classify_memory(content),
		"created_at": datetime.utcnow(),
	}


def save_memory(user_id: str, content: str, embedding: Iterable[float]) -> MemoryRecord:
	"""Save a memory into the shared in-memory store."""

	memory = _build_memory_record(user_id, content, embedding)
	_MEMORY_STORE.append(memory)
	return memory


def get_recent_memories(user_id: str, limit: int = 50) -> list[MemoryRecord]:
	"""Return the latest memories for a user from the shared store."""

	user_memories = [memory for memory in _MEMORY_STORE if memory.get("user_id") == user_id]
	user_memories.sort(key=lambda memory: memory.get("created_at") or datetime.min, reverse=True)
	return user_memories[:limit]


@dataclass(slots=True)
class MemoryService:
	"""In-memory memory service used until MongoDB is wired up."""

	storage: list[MemoryRecord] = field(default_factory=lambda: _MEMORY_STORE)

	def save_memory(self, user_id: str, content: str, embedding: Iterable[float]) -> MemoryRecord:
		"""Save a memory into the configured store."""

		memory = _build_memory_record(user_id, content, embedding)
		self.storage.append(memory)
		return memory

	def get_recent_memories(self, user_id: str, limit: int = 50) -> list[MemoryRecord]:
		"""Return the latest memories for a user."""

		user_memories = [memory for memory in self.storage if memory.get("user_id") == user_id]
		user_memories.sort(key=lambda memory: memory.get("created_at") or datetime.min, reverse=True)
		return user_memories[:limit]
