"""Agent Memory System for Cognet."""

from __future__ import annotations

from typing import Any


agent_memory: dict[str, list[dict[str, Any]]] = {
	"planner": [],
	"executor": [],
	"critic": [],
}


def store_agent_memory(agent_name: str, input_data: Any, output: Any) -> None:
	if agent_name not in agent_memory:
		agent_memory[agent_name] = []

	agent_memory[agent_name].append({
		"input": input_data,
		"output": output,
	})