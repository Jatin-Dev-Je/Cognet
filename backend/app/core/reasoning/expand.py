"""Context expansion for Cognet reasoning."""

from __future__ import annotations


def expand_context(chain: list[tuple[str, dict[str, object]]]) -> list[str]:
	return [str(memory.get("content", "")) for _, memory in chain if str(memory.get("content", "")).strip()]