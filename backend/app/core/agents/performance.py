"""Agent Performance Tracker for Cognet."""

from __future__ import annotations


agent_scores: dict[str, list[float]] = {
	"planner": [],
	"executor": [],
	"critic": [],
}


def update_score(agent_name: str, score: float) -> None:
	if agent_name not in agent_scores:
		agent_scores[agent_name] = []

	agent_scores[agent_name].append(score)


def average_score(agent_name: str) -> float:
	scores = agent_scores.get(agent_name, [])
	return sum(scores) / len(scores) if scores else 0.0