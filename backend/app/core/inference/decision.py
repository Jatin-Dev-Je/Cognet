"""Decision Engine for Cognet."""

from __future__ import annotations

from typing import Any, Mapping


def decide_action(fused: Mapping[str, Any]) -> str:
	intent = str(fused.get("intent") or "general")

	if intent == "ask_next_step":
		if fused.get("tasks"):
			return f"Focus on: {fused['tasks'][0]}"
		return "Define your next step clearly"

	if intent == "ask_status":
		return "You're actively progressing on your current work"

	if intent == "update_progress":
		return "Progress recorded. Move to next phase"

	if intent == "new_goal":
		return "Goal registered. Start with first actionable step"

	return "Continue your current work"