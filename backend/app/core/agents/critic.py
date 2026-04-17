"""Critic Agent for Cognet."""

from __future__ import annotations

from app.core.agents.base import BaseAgent


class CriticAgent(BaseAgent):
	"""Improve response quality."""

	def run(self, response: str) -> str:
		if "Define your next task" in response:
			return response + " — break it into a small actionable step"

		if response.startswith("Focus on"):
			return response + " — break it into a small actionable step"

		return response