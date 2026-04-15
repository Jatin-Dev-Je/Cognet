"""Response formatter for Cognet.

Purpose:
Standardize final assistant output into a consistent structure.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence


def _format_list(items: Sequence[Any]) -> str:
	if not items:
		return "- None"
	return "\n".join(f"- {item}" for item in items)


def format_response(data: Mapping[str, Any]) -> str:
	"""Format Cognet response data into a stable text response."""

	project = data.get("project") or "N/A"
	completed = _format_list(list(data.get("completed", [])))
	tasks = _format_list(list(data.get("tasks", [])))
	insights = list(data.get("insights", []))
	raw_response = data.get("raw_response") or "N/A"
	insight = data.get("insight") or (insights[0] if insights else raw_response)

	return f"""
Current Focus:
{project}

Completed:
{completed}

Next Steps:
{tasks}

Insight:
{insight}
""".strip()