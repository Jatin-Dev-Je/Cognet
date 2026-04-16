"""Pattern Detection Engine for Cognet."""

from __future__ import annotations

from typing import Any, Sequence


def detect_pattern(memories: Sequence[dict[str, Any]]) -> list[str]:
	contents = [str(memory.get("content", "")).lower() for memory in memories[-5:]]

	pattern: list[str] = []

	for content in contents:
		if "api" in content:
			pattern.append("api")
		elif "retrieval" in content:
			pattern.append("retrieval")
		elif "optimize" in content or "improve" in content:
			pattern.append("optimization")

	return pattern