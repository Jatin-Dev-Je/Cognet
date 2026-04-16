"""Agent Runner for Cognet.

Purpose:
Run all agents against the current context.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from app.domain.agent.entity import Agent
from app.core.prediction.proactive import run_prediction


def run_agents(context: Mapping[str, Any], agents: Sequence[Agent], memories: Sequence[dict[str, Any]] | None = None) -> list[str]:
	"""Run all agents and collect triggered actions."""

	results: list[str] = []
	prediction = run_prediction(memories or [])

	for agent in agents:
		if agent.active and agent.condition(context):
			results.append(agent.action(context))

	if prediction["confidence"] > 0.7 and prediction["prediction"]:
		results.append(f"Suggested next action: {prediction['prediction']}")

	return results