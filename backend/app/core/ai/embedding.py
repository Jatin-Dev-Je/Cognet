"""Embedding pipeline for Cognet."""

from __future__ import annotations

import asyncio
import hashlib
import re
from math import sqrt

from app.core.cache import cache_get, cache_key, cache_set


def _tokenize(text: str) -> list[str]:
	return re.findall(r"[a-z0-9]+", text.lower())


def _normalize(vector: list[float]) -> list[float]:
	magnitude = sqrt(sum(value * value for value in vector))
	if magnitude == 0:
		return vector
	return [value / magnitude for value in vector]


def generate_embedding(text: str, dimensions: int = 64) -> list[float]:
	cache_id = cache_key("embedding", text, dimensions)
	cached = cache_get(cache_id)
	if cached is not None:
		return list(cached)

	vector = [0.0] * dimensions
	for token in _tokenize(text):
		digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
		index = int(digest, 16) % dimensions
		vector[index] += 1.0

	normalized = _normalize(vector)
	cache_set(cache_id, list(normalized))
	return normalized


async def generate_embedding_async(text: str, dimensions: int = 64) -> list[float]:
	return await asyncio.to_thread(generate_embedding, text, dimensions)