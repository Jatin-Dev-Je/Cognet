"""Inference Engine for Cognet.

Purpose:
Analyze user context and generate predictions, suggestions, and insights.

Inputs:
- context: structured context from the context builder

Output:
- list[str]: concise insights that make responses feel intelligent

Steps:
- suggest the next step from pending work
- detect the current focus area
- warn when there are too many open tasks
- add a subtle confidence tone when the user is actively building
"""

from __future__ import annotations

from typing import Any, Mapping


def generate_insights(context: Mapping[str, Any]) -> list[str]:
	insights: list[str] = []

	project = context.get("project")
	pending = list(context.get("tasks", context.get("pending", [])))
	completed = list(context.get("completed", []))

	if pending:
		insights.append(f"Suggested next step: {pending[0]}")

	if project:
		insights.append(f"You are currently focused on: {project}")

	if completed:
		insights.append(f"You have already completed: {completed[0]}")

	if len(pending) > 2:
		insights.append("You have multiple pending tasks, consider prioritizing one.")

	if project and "building" in str(project).lower():
		insights.append("You're making solid progress - keep momentum.")

	return insights
