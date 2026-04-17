"""Memory Chain Builder for Cognet."""

from __future__ import annotations

from typing import Any, Sequence


def build_memory_chain(memories: Sequence[dict[str, Any]]) -> list[tuple[str, dict[str, Any]]]:
	chain: list[tuple[str, dict[str, Any]]] = []

	for memory in memories:
		content = str(memory.get("content", "")).lower()

		if "api" in content:
			chain.append(("api", memory))
		elif "retrieval" in content:
			chain.append(("retrieval", memory))
		elif "optimize" in content or "performance" in content:
			chain.append(("optimization", memory))
		elif "test" in content:
			chain.append(("testing", memory))

	return chain