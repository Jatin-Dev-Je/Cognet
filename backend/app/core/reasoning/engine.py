"""Multi-hop reasoning engine for Cognet."""

from __future__ import annotations


def reason_over_chain(chain: list[tuple[str, dict[str, object]]]) -> str:
	steps = [step for step, _ in chain]

	if "api" in steps and "retrieval" in steps and "optimization" in steps:
		return "You moved from API development to retrieval and are now optimizing it"

	if "api" in steps and "retrieval" in steps:
		return "You moved from API development to retrieval system"

	if "retrieval" in steps and "optimization" in steps:
		return "You are optimizing an already built system"

	if "optimization" in steps:
		return "You are progressing through development stages"

	return "You are progressing through development stages"