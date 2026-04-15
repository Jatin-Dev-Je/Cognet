"""Semantic Retrieval Engine for Cognet.

Purpose:
Retrieve the most relevant memories using embedding similarity.

Inputs:
- query_embedding: vector representation of the current query
- memories: iterable of memory documents with stored embeddings
- top_k: number of memories to return

Output:
- list of the top relevant memory documents in descending relevance order

Steps:
- compare the query embedding with each memory embedding
- score each memory using cosine similarity
- sort by score
- return the top matches
"""

from __future__ import annotations

from math import sqrt
from typing import Any, Mapping, Sequence


MemoryDocument = Mapping[str, Any]


def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
	"""Return cosine similarity between two vectors."""

	if len(a) != len(b):
		raise ValueError("Embedding vectors must have the same length.")

	dot_product = sum(left * right for left, right in zip(a, b))
	magnitude_a = sqrt(sum(value * value for value in a))
	magnitude_b = sqrt(sum(value * value for value in b))

	if magnitude_a == 0 or magnitude_b == 0:
		return 0.0

	return dot_product / (magnitude_a * magnitude_b)


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
	"""Return the top_k most relevant memories for the query."""

	scored_memories: list[tuple[float, dict[str, Any]]] = []

	for memory in memories:
		memory_embedding = _extract_embedding(memory)
		if len(memory_embedding) != len(query_embedding):
			continue

		score = cosine_similarity(query_embedding, memory_embedding)
		scored_memories.append((score, dict(memory)))

	scored_memories.sort(key=lambda item: item[0], reverse=True)

	return [memory for _, memory in scored_memories[:top_k]]
