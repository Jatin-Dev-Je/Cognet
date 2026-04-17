"""Agent selector for Cognet."""

from __future__ import annotations

from typing import Any, Mapping

from app.core.agents.executor_types import InsightExecutor, TaskExecutor


def select_executor(context: Mapping[str, Any]):
	if context.get("tasks"):
		return TaskExecutor()

	return InsightExecutor()