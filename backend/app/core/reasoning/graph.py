"""Reasoning graph builder for Cognet."""

from __future__ import annotations


def build_reasoning_graph(chain: list[tuple[str, dict[str, object]]]) -> dict[str, list[str]]:
	nodes = [step for step, _ in chain]
	edges: list[str] = []

	for index in range(len(nodes) - 1):
		edges.append(f"{nodes[index]} -> {nodes[index + 1]}")

	return {
		"nodes": nodes,
		"edges": edges,
	}