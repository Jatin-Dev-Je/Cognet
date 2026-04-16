"""Next Step Engine for Cognet."""

from __future__ import annotations

from typing import Any, Mapping


def suggest_next(context: Mapping[str, Any]) -> str:
	tasks = list(context.get("tasks", []))
	completed = list(context.get("completed", []))

	if tasks:
		return f"Focus on: {tasks[0]}"

	if completed:
		return "Build on your last completed work"

	return "Define your next goal"