"""Context Builder for Cognet.

Purpose:
Convert raw memories into structured context for downstream reasoning.

Inputs:
- memories: relevant memory documents

Output:
- dict: structured context with project, completed work, pending work, and suggestions

Steps:
- inspect each memory
- classify it into project, completed, or pending work
- derive a simple suggestion from the pending items
- format the structured data for AI consumption
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence


MemoryDocument = Mapping[str, Any]


def build_context(memories: Sequence[MemoryDocument]) -> dict[str, Any]:
	"""Build structured context from relevant memories."""

	context: dict[str, Any] = {
		"project": None,
		"completed": [],
		"pending": [],
	}

	for memory in memories:
		content = str(memory.get("content", "")).strip()
		if not content:
			continue

		lowered = content.lower()

		if "building" in lowered or "working on" in lowered:
			context["project"] = content
		elif "done" in lowered or "completed" in lowered:
			context["completed"].append(content)
		else:
			context["pending"].append(content)

	if context["pending"]:
		context["suggestion"] = context["pending"][0]
	else:
		context["suggestion"] = "Continue the current project with the next logical step."

	return context


def format_context(context: Mapping[str, Any]) -> str:
	"""Format structured context for AI prompts."""

	formatted = ""

	project = context.get("project")
	completed = list(context.get("completed", []))
	pending = list(context.get("pending", []))
	suggestion = context.get("suggestion")

	if project:
		formatted += f"Current Project:\n{project}\n\n"

	if completed:
		formatted += "Completed:\n"
		for item in completed:
			formatted += f"- {item}\n"

	if pending:
		formatted += "\nPending:\n"
		for item in pending:
			formatted += f"- {item}\n"

	if suggestion:
		formatted += f"\nSuggested Next Step:\n- {suggestion}\n"

	return formatted.strip()
