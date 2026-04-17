"""Planner Agent for Cognet."""

from __future__ import annotations

from typing import Any, Mapping

from app.core.agents.base import BaseAgent


class PlannerAgent(BaseAgent):
	"""Decide a plan based on intent, time, and prediction."""

	def run(self, fused_context: Mapping[str, Any]) -> dict[str, Any]:
		intent = str(fused_context.get("intent") or "general")
		prediction = dict(fused_context.get("prediction") or {})

		if intent == "ask_next_step":
			return {
				"plan": "determine next actionable task",
				"prediction": prediction,
			}

		if intent == "ask_status":
			return {
				"plan": "summarize current progress",
				"prediction": prediction,
			}

		return {
			"plan": "general reasoning",
			"prediction": prediction,
		}