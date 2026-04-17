"""Specialized executors for Cognet."""

from __future__ import annotations

from typing import Any, Mapping

from app.core.agents.base import BaseAgent


class TaskExecutor(BaseAgent):
	def run(self, context: Mapping[str, Any]):
		tasks = list(context.get("tasks", []))
		if tasks:
			return f"Focus on {tasks[0]}"
		return None


class InsightExecutor(BaseAgent):
	def run(self, context: Mapping[str, Any]):
		return "You are progressing logically"