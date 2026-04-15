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

from app.core.inference.classifier import assign_memory_level, classify_memory, compute_importance
from app.utils.logger import logger


MemoryRecord = dict[str, Any]
_MEMORY_STORE: list[MemoryRecord] = []


def is_duplicate(user_id: str, content: str, session_id: str | None = None) -> bool:
	"""Check whether the same memory already exists."""

	for memory in _MEMORY_STORE:
		if memory.get("user_id") != user_id:
			continue
		if session_id is not None and memory.get("session_id") != session_id:
			continue
		if memory.get("content") == content:
			return True
	return False


def _build_memory_record(
	user_id: str,
	content: str,
	embedding: Iterable[float],
	session_id: str | None = None,
	goal: str | None = None,
) -> MemoryRecord:
	"""Build a memory record with classification and timestamps."""

	memory_type = classify_memory(content)

	return {
		"user_id": user_id,
		"session_id": session_id,
		"goal": goal,
		"content": content,
		"embedding": list(embedding),
		"type": memory_type,
		"importance": compute_importance(memory_type),
		"memory_level": assign_memory_level(memory_type),
		"created_at": datetime.utcnow(),
	}


def save_memory(
	user_id: str,
	content: str,
	embedding: Iterable[float],
	session_id: str | None = None,
	goal: str | None = None,
) -> MemoryRecord:
	"""Save a memory into the shared in-memory store."""

	if is_duplicate(user_id, content, session_id=session_id):
		logger.info("Skipping duplicate memory for user_id=%s", user_id)
		return next(
			memory
			for memory in _MEMORY_STORE
			if memory.get("user_id") == user_id
			and memory.get("content") == content
			and (session_id is None or memory.get("session_id") == session_id)
		)

	memory = _build_memory_record(user_id, content, embedding, session_id=session_id, goal=goal)
	_MEMORY_STORE.append(memory)
	logger.info("Saving memory for user_id=%s", user_id)
	return memory


def get_recent_memories(user_id: str, limit: int = 50, session_id: str | None = None) -> list[MemoryRecord]:
	"""Return the latest memories for a user from the shared store."""

	user_memories = [
		memory
		for memory in _MEMORY_STORE
		if memory.get("user_id") == user_id and (session_id is None or memory.get("session_id") == session_id)
	]
	user_memories.sort(key=lambda memory: memory.get("created_at") or datetime.min, reverse=True)
	return user_memories[:limit]


@dataclass(slots=True)
class MemoryService:
	"""In-memory memory service used until MongoDB is wired up."""

	storage: list[MemoryRecord] = field(default_factory=lambda: _MEMORY_STORE)

	def save_memory(
		self,
		user_id: str,
		content: str,
		embedding: Iterable[float],
		session_id: str | None = None,
		goal: str | None = None,
	) -> MemoryRecord:
		"""Save a memory into the configured store."""

		if is_duplicate(user_id, content, session_id=session_id):
			logger.info("Skipping duplicate memory for user_id=%s", user_id)
			return next(
				memory
				for memory in self.storage
				if memory.get("user_id") == user_id
				and memory.get("content") == content
				and (session_id is None or memory.get("session_id") == session_id)
			)

		memory = _build_memory_record(user_id, content, embedding, session_id=session_id, goal=goal)
		self.storage.append(memory)
		logger.info("Saving memory for user_id=%s", user_id)
		return memory

	def get_recent_memories(self, user_id: str, limit: int = 50, session_id: str | None = None) -> list[MemoryRecord]:
		"""Return the latest memories for a user."""

		user_memories = [
			memory
			for memory in self.storage
			if memory.get("user_id") == user_id and (session_id is None or memory.get("session_id") == session_id)
		]
		user_memories.sort(key=lambda memory: memory.get("created_at") or datetime.min, reverse=True)
		return user_memories[:limit]
