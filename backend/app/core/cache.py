"""Simple in-memory cache for Cognet.

Purpose:
Provide a lightweight cache for embeddings and recent context until Redis is introduced.
"""

from __future__ import annotations

from typing import Any


cache: dict[str, Any] = {}


def cache_key(*parts: object) -> str:
	return ":".join(str(part) for part in parts)


def cache_get(key: str) -> Any | None:
	return cache.get(key)


def cache_set(key: str, value: Any) -> Any:
	cache[key] = value
	return value


def cache_invalidate_prefix(prefix: str) -> None:
	for key in [item_key for item_key in list(cache) if item_key.startswith(prefix)]:
		cache.pop(key, None)