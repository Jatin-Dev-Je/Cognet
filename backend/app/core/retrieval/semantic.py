"""Hybrid Retrieval Engine for Cognet.

Purpose:
Retrieve relevant memories using semantic similarity and recency scoring.

Steps:
1. compute cosine similarity
2. compute recency score
3. combine scores
4. sort and return top results
"""

from __future__ import annotations

from datetime import datetime
from math import sqrt
from typing import Any, Mapping, Sequence


MemoryDocument = Mapping[str, Any]


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
	"""Compute cosine similarity between two vectors."""

	if len(a) != len(b):
		raise ValueError("Embedding vectors must have the same length.")

	dot_product = sum(left * right for left, right in zip(a, b))
	magnitude_a = sqrt(sum(value * value for value in a))
	magnitude_b = sqrt(sum(value * value for value in b))

	if magnitude_a == 0 or magnitude_b == 0:
		return 0.0

	return dot_product / (magnitude_a * magnitude_b)


def compute_score(memory: MemoryDocument, similarity: float) -> float:
	"""Compute a hybrid score combining similarity and recency."""

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

	return 0.6 * similarity + 0.2 * recency + 0.2 * importance


def _extract_embedding(memory: MemoryDocument) -> Sequence[float]:
	embedding = memory.get("embedding")
	if not isinstance(embedding, Sequence):
		return []
	return embedding


def get_relevant_memories(
	query_embedding: Sequence[float],
	memories: Sequence[MemoryDocument],
	top_k: int = 5,
) -> list[dict[str, Any]]:
	"""Retrieve the top relevant memories using hybrid scoring."""

	scored_memories: list[tuple[float, dict[str, Any]]] = []

	for memory in memories:
		memory_embedding = _extract_embedding(memory)
		if len(memory_embedding) != len(query_embedding):
			continue

		similarity = cosine_similarity(query_embedding, memory_embedding)
		score = compute_score(memory, similarity)
		scored_memories.append((score, dict(memory)))

	scored_memories.sort(key=lambda item: item[0], reverse=True)

	return [memory for _, memory in scored_memories[:top_k]]
