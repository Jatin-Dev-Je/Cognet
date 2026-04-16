"""Memory service for Cognet.

Memory Persistence Rules:
Purpose:
Ensure all user data is stored in MongoDB and survives restarts.

Requirements:

Validation:
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import asyncio
from typing import Any, Iterable

from app.core.cache import cache_get, cache_invalidate_prefix, cache_key, cache_set
from app.core.config.flags import FEATURES
from app.core.events.event_bus import event_bus
from app.core.identity import generate_id
from app.core.inference.classifier import assign_memory_level, classify_memory, compute_importance
from app.core.memory.summarizer import summarize_memories
from app.core.utils.sanitize import clean_input
from app.infrastructure.db.mongo.base_repository import MongoRepository
from app.infrastructure.db.mongo.collections import memory_collection
from app.utils.logger import logger
from app.domain.memory.entity import enrich_temporal_memory, soft_delete_memory


MemoryRecord = dict[str, Any]
_MEMORY_STORE: list[MemoryRecord] = []
_CACHE_PREFIX = "recent_memories"


def _memory_query(user_id: str, content: str, session_id: str | None = None) -> dict[str, Any]:
	query: dict[str, Any] = {"user_id": user_id, "content": content}
	if session_id is not None:
		query["session_id"] = session_id
	return query


def _build_memory_record(
	user_id: str,
	content: str,
	embedding: Iterable[float],
	session_id: str | None = None,
	goal: str | None = None,
) -> MemoryRecord:
	"""Build a memory record with classification and timestamps."""

	memory_type = classify_memory(content)
	memory: MemoryRecord = {
		"id": generate_id(),
		"user_id": user_id,
		"session_id": session_id,
		"goal": goal,
		"content": content,
		"embedding": list(embedding),
		"type": memory_type,
		"importance": compute_importance(memory_type),
		"memory_level": assign_memory_level(memory_type),
		"version": 1,
		"is_deleted": False,
	}
	return enrich_temporal_memory(memory)


class MongoMemoryRepository(MongoRepository):
	"""Mongo-backed memory repository."""

	def __init__(self) -> None:
		super().__init__(memory_collection)

	def save_memory(
		self,
		user_id: str,
		content: str,
		embedding: Iterable[float],
		session_id: str | None = None,
		goal: str | None = None,
	) -> MemoryRecord:
		"""Insert a memory record into MongoDB or return the existing duplicate."""

		try:
			content = clean_input(content)
			existing = self.find_one(_memory_query(user_id, content, session_id=session_id))
			if existing is not None:
				logger.info("Skipping duplicate memory for user_id=%s", user_id)
				return existing

			memory = _build_memory_record(user_id, content, embedding, session_id=session_id, goal=goal)
			stored_memory = self.insert_one(memory)
			event_bus.publish("memory_created", stored_memory)
			cache_invalidate_prefix(_CACHE_PREFIX)
			logger.info("Saving memory for user_id=%s", user_id)
			self._enforce_memory_limit(user_id)
			return stored_memory
		except Exception as exc:
			logger.warning("Mongo unavailable, using fallback memory store: %s", exc)
			return self._fallback_save(user_id, content, embedding, session_id=session_id, goal=goal)

	def get_recent_memories(self, user_id: str, limit: int = 50, session_id: str | None = None) -> list[MemoryRecord]:
		"""Return the latest memories for a user from MongoDB."""

		query: dict[str, Any] = {"user_id": user_id}
		if session_id is not None:
			query["session_id"] = session_id
		try:
			cache_id = cache_key(_CACHE_PREFIX, user_id, limit, session_id)
			cached = cache_get(cache_id)
			if cached is not None:
				return [memory for memory in list(cached) if not memory.get("is_deleted")]
			memories = [memory for memory in self.find_many(query, limit=limit, sort=[("created_at", -1)]) if not memory.get("is_deleted")]
			cache_set(cache_id, list(memories))
			return memories
		except Exception as exc:
			logger.warning("Mongo unavailable, reading fallback memory store: %s", exc)
			return self._fallback_recent(user_id, limit=limit, session_id=session_id)

	async def save_memory_async(
		self,
		user_id: str,
		content: str,
		embedding: Iterable[float],
		session_id: str | None = None,
		goal: str | None = None,
	) -> MemoryRecord:
		return await asyncio.to_thread(self.save_memory, user_id, content, embedding, session_id, goal)

	async def get_recent_memories_async(self, user_id: str, limit: int = 50, session_id: str | None = None) -> list[MemoryRecord]:
		return await asyncio.to_thread(self.get_recent_memories, user_id, limit, session_id)

	def _fallback_save(
		self,
		user_id: str,
		content: str,
		embedding: Iterable[float],
		session_id: str | None = None,
		goal: str | None = None,
	) -> MemoryRecord:
		for memory in _MEMORY_STORE:
			if memory.get("user_id") == user_id and memory.get("content") == content and memory.get("session_id") == session_id:
				return memory

		memory = _build_memory_record(user_id, content, embedding, session_id=session_id, goal=goal)
		_MEMORY_STORE.append(memory)
		event_bus.publish("memory_created", memory)
		self._enforce_memory_limit(user_id)
		return memory

	def _fallback_recent(self, user_id: str, limit: int = 50, session_id: str | None = None) -> list[MemoryRecord]:
		filtered = [
			memory
			for memory in _MEMORY_STORE
			if memory.get("user_id") == user_id and (session_id is None or memory.get("session_id") == session_id) and not memory.get("is_deleted")
		]
		return filtered[-limit:]

	def _enforce_memory_limit(self, user_id: str) -> None:
		active_memories = [memory for memory in self.get_recent_memories(user_id, limit=2000) if not memory.get("is_deleted")]
		if len(active_memories) <= 1000:
			return

		overflow = active_memories[:-1000]
		if not overflow:
			return

		if FEATURES.get("summarization", True):
			summary_text = summarize_memories(overflow[:20])
			archive = _build_memory_record(
				user_id,
				f"Archived memory summary: {summary_text}",
				[0.0] * len(overflow[0].get("embedding", [0.0])),
				goal="memory_archive",
			)
			archive["memory_level"] = "long"
			_MEMORY_STORE.append(archive)

		for memory in overflow:
			soft_delete_memory(memory)
		cache_invalidate_prefix(_CACHE_PREFIX)


class InMemoryMemoryRepository:
	"""Legacy test-only repository adapter."""

	def __init__(self, storage: list[MemoryRecord]) -> None:
		self.storage = storage

	def save_memory(
		self,
		user_id: str,
		content: str,
		embedding: Iterable[float],
		session_id: str | None = None,
		goal: str | None = None,
	) -> MemoryRecord:
		memory = _build_memory_record(user_id, content, embedding, session_id=session_id, goal=goal)
		self.storage.append(memory)
		event_bus.publish("memory_created", memory)
		cache_invalidate_prefix(_CACHE_PREFIX)
		return memory

	def get_recent_memories(self, user_id: str, limit: int = 50, session_id: str | None = None) -> list[MemoryRecord]:
		filtered = [
			memory
			for memory in self.storage
			if memory.get("user_id") == user_id and (session_id is None or memory.get("session_id") == session_id) and not memory.get("is_deleted")
		]
		return filtered[-limit:]

	async def save_memory_async(
		self,
		user_id: str,
		content: str,
		embedding: Iterable[float],
		session_id: str | None = None,
		goal: str | None = None,
	) -> MemoryRecord:
		return await asyncio.to_thread(self.save_memory, user_id, content, embedding, session_id, goal)

	async def get_recent_memories_async(self, user_id: str, limit: int = 50, session_id: str | None = None) -> list[MemoryRecord]:
		return await asyncio.to_thread(self.get_recent_memories, user_id, limit, session_id)


@dataclass(slots=True)
class MemoryService:
	"""Mongo-backed memory service."""

	repository: MongoMemoryRepository | InMemoryMemoryRepository | None = None
	storage: list[MemoryRecord] | None = None

	def __post_init__(self) -> None:
		if self.repository is None:
			if self.storage is not None:
				self.repository = InMemoryMemoryRepository(self.storage)
			else:
				self.repository = MongoMemoryRepository()

	def save_memory(
		self,
		user_id: str,
		content: str,
		embedding: Iterable[float],
		session_id: str | None = None,
		goal: str | None = None,
	) -> MemoryRecord:
		"""Save a memory into MongoDB."""

		assert self.repository is not None
		return self.repository.save_memory(user_id, content, embedding, session_id=session_id, goal=goal)

	async def save_memory_async(
		self,
		user_id: str,
		content: str,
		embedding: Iterable[float],
		session_id: str | None = None,
		goal: str | None = None,
	) -> MemoryRecord:
		assert self.repository is not None
		return await self.repository.save_memory_async(user_id, content, embedding, session_id=session_id, goal=goal)

	def get_recent_memories(self, user_id: str, limit: int = 50, session_id: str | None = None) -> list[MemoryRecord]:
		"""Return the latest memories for a user."""

		assert self.repository is not None
		return self.repository.get_recent_memories(user_id, limit=limit, session_id=session_id)

	async def get_recent_memories_async(self, user_id: str, limit: int = 50, session_id: str | None = None) -> list[MemoryRecord]:
		assert self.repository is not None
		return await self.repository.get_recent_memories_async(user_id, limit=limit, session_id=session_id)


_DEFAULT_MEMORY_SERVICE = MemoryService()


def save_memory(
	user_id: str,
	content: str,
	embedding: Iterable[float],
	session_id: str | None = None,
	goal: str | None = None,
) -> MemoryRecord:
	"""Save a memory using the default Mongo-backed service."""

	return _DEFAULT_MEMORY_SERVICE.save_memory(user_id, content, embedding, session_id=session_id, goal=goal)


async def save_memory_async(
	user_id: str,
	content: str,
	embedding: Iterable[float],
	session_id: str | None = None,
	goal: str | None = None,
) -> MemoryRecord:
	return await _DEFAULT_MEMORY_SERVICE.save_memory_async(user_id, content, embedding, session_id=session_id, goal=goal)


def get_recent_memories(user_id: str, limit: int = 50, session_id: str | None = None) -> list[MemoryRecord]:
	"""Return recent memories using the default Mongo-backed service."""

	return _DEFAULT_MEMORY_SERVICE.get_recent_memories(user_id, limit=limit, session_id=session_id)


async def get_recent_memories_async(user_id: str, limit: int = 50, session_id: str | None = None) -> list[MemoryRecord]:
	return await _DEFAULT_MEMORY_SERVICE.get_recent_memories_async(user_id, limit=limit, session_id=session_id)
