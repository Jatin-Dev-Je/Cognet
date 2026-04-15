"""Context Builder for Cognet.

Purpose:
Convert structured memories into organized context.

Output:
{
	project: str
	completed: list
	tasks: list
}
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from app.core.inference.classifier import classify_memory


MemoryDocument = Mapping[str, Any]


def build_context(memories: Sequence[MemoryDocument]) -> dict[str, Any]:
	"""Build structured context from relevant memories."""

	context: dict[str, Any] = {
		"project": None,
		"completed": [],
		"tasks": [],
	}

	for memory in memories:
		content = str(memory.get("content", "")).strip()
		if not content:
			continue

		memory_type = str(memory.get("type") or classify_memory(content))

		if memory_type == "project":
			context["project"] = content
		elif memory_type == "completed":
			context["completed"].append(content)
		else:
			context["tasks"].append(content)

	if context["tasks"]:
		context["suggestion"] = context["tasks"][0]
	else:
		context["suggestion"] = "Continue the current project with the next logical step."

	return context


def format_context(context: Mapping[str, Any]) -> str:
	"""Format structured context for AI prompts."""

	formatted = ""

	project = context.get("project")
	completed = list(context.get("completed", []))
	pending = list(context.get("tasks", []))
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
