"""Context formatter for Cognet."""

from __future__ import annotations


def clean_output(text: str) -> str:
	"""Trim generated text for stable output."""

	return text.strip()


def format_temporal_context(time_data: dict[str, list[str]]) -> str:
	text = ""

	if time_data["today"]:
		text += "Today:\n"
		for item in time_data["today"]:
			text += f"- {item}\n"

	if time_data["yesterday"]:
		text += "\nYesterday:\n"
		for item in time_data["yesterday"]:
			text += f"- {item}\n"

	if time_data["this_week"]:
		text += "\nThis Week:\n"
		for item in time_data["this_week"]:
			text += f"- {item}\n"

	return text.strip()