"""Trigger Engine for Cognet autonomous mode."""

from __future__ import annotations

from typing import Any, Mapping


def should_trigger(memory: Mapping[str, Any] | None) -> bool:
	if not memory:
		return False

	if memory.get("type") in ["project", "task"]:
		return True

	return False