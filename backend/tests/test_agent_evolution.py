from __future__ import annotations

from app.core.agents.evolution import evolve_agents
from app.core.agents.executor_types import InsightExecutor, TaskExecutor
from app.core.agents.memory import agent_memory, store_agent_memory
from app.core.agents.performance import agent_scores, average_score, update_score
from app.core.agents.selector import select_executor


def _reset_agent_state() -> None:
	for key in agent_memory:
		agent_memory[key] = []
	for key in agent_scores:
		agent_scores[key] = []


def test_agent_memory_records_inputs_and_outputs() -> None:
	_reset_agent_state()
	store_agent_memory("planner", {"intent": "ask_next_step"}, {"plan": "determine next actionable task"})

	assert agent_memory["planner"]
	assert agent_memory["planner"][0]["input"]["intent"] == "ask_next_step"


def test_performance_tracker_averages_scores() -> None:
	_reset_agent_state()
	update_score("executor", 0.5)
	update_score("executor", 1.0)

	assert average_score("executor") == 0.75


def test_selector_chooses_task_executor_when_tasks_exist() -> None:
	_reset_agent_state()
	executor = select_executor({"tasks": ["Improve retrieval"]})

	assert isinstance(executor, TaskExecutor)


def test_selector_chooses_insight_executor_when_no_tasks() -> None:
	_reset_agent_state()
	executor = select_executor({"tasks": []})

	assert isinstance(executor, InsightExecutor)


def test_evolution_switches_strategy_on_low_executor_score() -> None:
	_reset_agent_state()
	agent_scores["executor"] = [0.2]

	assert evolve_agents() == "switch_strategy"