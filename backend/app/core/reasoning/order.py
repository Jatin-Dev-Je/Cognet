"""Chain ordering helpers for Cognet."""

from __future__ import annotations


ORDER = ["api", "retrieval", "optimization", "testing"]


def sort_chain(chain: list[tuple[str, dict[str, object]]]) -> list[tuple[str, dict[str, object]]]:
	return sorted(chain, key=lambda item: ORDER.index(item[0]) if item[0] in ORDER else 99)