"""Action Executor for Cognet autonomous mode."""

from __future__ import annotations

from typing import Any, Mapping


def execute_action(action: Mapping[str, Any] | None) -> str | None:
	if not action:
		return None

	if action.get("type") == "suggest_next":
		return f"Autonomous Suggestion: {action['payload']}"

	if action.get("type") == "remind":
		return f"Reminder: {action['payload']}"

	return None