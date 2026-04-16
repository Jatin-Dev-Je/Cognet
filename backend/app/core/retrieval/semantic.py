"""Hybrid Retrieval Engine for Cognet."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from app.core.retrieval.scoring import compute_score, cosine_similarity


MemoryDocument = Mapping[str, Any]


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
