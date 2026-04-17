"""Action layer for Cognet."""

from __future__ import annotations


def act(plan_step: str, context: dict[str, object] | None = None) -> str:
	return f"Next Step: {plan_step}"