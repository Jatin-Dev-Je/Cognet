"""Memory layer for Cognet."""

from __future__ import annotations

from typing import Any, Sequence

from app.core.context.temporal_builder import group_by_time


def get_memory_state(memories: Sequence[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, list[str]]]:
	memory_list = list(memories)
	temporal = group_by_time(memory_list)
	return memory_list, temporal