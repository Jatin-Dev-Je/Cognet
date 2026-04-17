"""Executor Agent for Cognet."""

from __future__ import annotations

from typing import Any, Mapping

from app.core.agents.base import BaseAgent


class ExecutorAgent(BaseAgent):
	"""Execute the selected plan and generate a response."""

	def run(self, plan: Mapping[str, Any], context: Mapping[str, Any]) -> str:
		plan_name = str(plan.get("plan") or "general reasoning")
		tasks = list(context.get("tasks", []))

		if plan_name == "determine next actionable task":
			if tasks:
				return f"Focus on {tasks[0]}"
			return "Define your next task"

		if plan_name == "summarize current progress":
			return "You are making consistent progress"

		return "Continue your current work"