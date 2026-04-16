"""Temporal retrieval scoring for Cognet."""

from __future__ import annotations

from datetime import datetime
from math import sqrt
from typing import Any, Mapping, Sequence


MemoryDocument = Mapping[str, Any]


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
	if len(a) != len(b):
		raise ValueError("Embedding vectors must have the same length.")

	dot_product = sum(left * right for left, right in zip(a, b))
	magnitude_a = sqrt(sum(value * value for value in a))
	magnitude_b = sqrt(sum(value * value for value in b))

	if magnitude_a == 0 or magnitude_b == 0:
		return 0.0

	return dot_product / (magnitude_a * magnitude_b)


def temporal_score(memory: MemoryDocument) -> float:
	bucket = str(memory.get("day_bucket") or "older")
	if bucket == "today":
		return 1.0
	if bucket == "yesterday":
		return 0.8
	if bucket == "this_week":
		return 0.6
	return 0.3


def compute_score(memory: MemoryDocument, similarity: float) -> float:
	created_at = memory.get("created_at")
	recency = 0.0

	if isinstance(created_at, str):
		try:
			created_at = datetime.fromisoformat(created_at)
		except ValueError:
			created_at = None

	if isinstance(created_at, datetime):
		time_difference = abs((datetime.utcnow() - created_at).total_seconds())
		recency = 1 / (1 + time_difference)

	importance = float(memory.get("importance") or 0.5)

	return 0.5 * similarity + 0.2 * recency + 0.2 * importance + 0.1 * temporal_score(memory)