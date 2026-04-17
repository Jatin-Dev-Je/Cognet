"""Role Evolution Engine for Cognet."""

from __future__ import annotations

from app.core.agents.performance import average_score


def evolve_agents() -> str:
	if average_score("executor") < 0.5:
		return "switch_strategy"

	return "stable"