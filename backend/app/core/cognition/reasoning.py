"""Reasoning layer for Cognet."""

from __future__ import annotations

from typing import Any, Sequence

from app.core.reasoning.chain import build_memory_chain
from app.core.reasoning.engine import reason_over_chain
from app.core.reasoning.expand import expand_context
from app.core.reasoning.graph import build_reasoning_graph
from app.core.reasoning.insight import generate_insight
from app.core.reasoning.order import sort_chain


def reason(memories: Sequence[dict[str, Any]]) -> dict[str, Any]:
	chain = build_memory_chain(memories)
	ordered = sort_chain(chain)
	return {
		"chain": chain,
		"ordered": ordered,
		"reasoning": reason_over_chain(ordered),
		"insight": generate_insight(ordered),
		"expanded_context": expand_context(ordered),
		"graph": build_reasoning_graph(ordered),
	}