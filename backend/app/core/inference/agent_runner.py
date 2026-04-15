"""Agent Runner for Cognet.

Purpose:
Run all agents against the current context.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from app.domain.agent.entity import Agent


def run_agents(context: Mapping[str, Any], agents: Sequence[Agent]) -> list[str]:
	"""Run all agents and collect triggered actions."""

	results: list[str] = []

	for agent in agents:
		if agent.active and agent.condition(context):
			results.append(agent.action(context))

	return results