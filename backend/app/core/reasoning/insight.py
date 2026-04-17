"""Insight generator for Cognet reasoning."""

from __future__ import annotations


def generate_insight(chain: list[tuple[str, dict[str, object]]]) -> str:
	steps = [step for step, _ in chain]

	if steps == ["api", "retrieval", "optimization"]:
		return "You are following a complete backend development lifecycle"

	if "optimization" in steps:
		return "You are refining system performance"

	return "You are building progressively"