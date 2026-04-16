"""Final temporal + intent response formatter for Cognet."""

from __future__ import annotations

from typing import Any, Mapping


def format_final(fused: Mapping[str, Any], decision: str) -> str:
	text = ""
	temporal = dict(fused.get("temporal", {}))

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

	text += f"\nNext Step:\n{decision}\n"
	return text.strip()