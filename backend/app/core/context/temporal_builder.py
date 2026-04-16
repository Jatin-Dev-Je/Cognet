"""Temporal Context Builder for Cognet."""

from __future__ import annotations

from typing import Any, Mapping, Sequence


MemoryDocument = Mapping[str, Any]


def group_by_time(memories: Sequence[MemoryDocument]) -> dict[str, list[str]]:
	result = {
		"today": [],
		"yesterday": [],
		"this_week": [],
	}

	for memory in memories:
		bucket = str(memory.get("day_bucket") or "")
		if bucket in result:
			content = str(memory.get("content", "")).strip()
			if content:
				result[bucket].append(content)

	return result