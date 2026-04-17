"""Final temporal + intent response formatter for Cognet."""

from __future__ import annotations

from typing import Any, Mapping


def format_final(
	fused: Mapping[str, Any],
	decision: str,
	prediction: str | None = None,
	reasoning: str | None = None,
	insight: str | None = None,
	completed: list[str] | None = None,
) -> str:
	text = ""
	temporal = dict(fused.get("temporal", {}))
	completed_items = list(completed or fused.get("completed", []))

	if temporal.get("today"):
		text += "Today:\n"
		for item in temporal["today"]:
			text += f"- {item}\n"

	if temporal.get("yesterday"):
		text += "\nYesterday:\n"
		for item in temporal["yesterday"]:
			text += f"- {item}\n"

	if temporal.get("this_week"):
		text += "\nThis Week:\n"
		for item in temporal["this_week"]:
			text += f"- {item}\n"

	if not text:
		for item in list(fused.get("recent", [])):
			text += f"- {item}\n"

	if completed_items:
		text += "\nCompleted:\n"
		for item in completed_items:
			text += f"- {item}\n"

	if reasoning:
		text += f"\nReasoning:\n{reasoning}\n"

	text += f"\nNext Step:\n{decision}\n"

	if prediction:
		text += f"\nPrediction:\n{prediction}\n"

	if insight:
		text += f"\nInsight:\n{insight}\n"

	return text.strip()