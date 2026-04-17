from __future__ import annotations

from app.core.cognition.action import act
from app.core.cognition.brain import run_cognition
from app.core.cognition.learning import learning_log
from app.core.cognition.memory import get_memory_state
from app.core.cognition.perception import perceive_input
from app.core.cognition.planning import plan
from app.core.cognition.reasoning import reason


def test_perception_cleans_input_and_detects_intent() -> None:
	result = perceive_input("  What should I do next?  ")

	assert result["clean_text"] == "What should I do next?"
	assert result["intent"] == "ask_next_step"


def test_memory_layer_returns_temporal_state() -> None:
	memories, temporal = get_memory_state([
		{"content": "I completed API", "day_bucket": "today"},
		{"content": "I worked on retrieval", "day_bucket": "yesterday"},
	])

	assert len(memories) == 2
	assert temporal["today"] == ["I completed API"]


def test_reasoning_layer_builds_chain_and_insight() -> None:
	result = reason([
		{"content": "I completed API"},
		{"content": "I worked on retrieval"},
		{"content": "I am optimizing performance"},
	])

	assert result["reasoning"] == "You moved from API development to retrieval and are now optimizing it"
	assert result["insight"] == "You are following a complete backend development lifecycle"


def test_planning_and_action_layers_use_prediction_or_tasks() -> None:
	assert plan({"tasks": ["Test system under real load"]}, None) == "Test system under real load"
	assert act("Test system under real load", {}) == "Next Step: Test system under real load"


def test_brain_runs_full_cognition_loop() -> None:
	learning_log.clear()
	result = run_cognition(
		"user-1",
		"I completed API and worked on retrieval",
		memories=[
			{"content": "I completed API", "day_bucket": "today"},
			{"content": "I worked on retrieval", "day_bucket": "today"},
			{"content": "I am optimizing performance", "day_bucket": "today"},
		],
		context={"tasks": ["Test system under real load"], "completed": ["API", "retrieval"]},
	)

	assert result["reasoning"]
	assert result["insight"]
	assert result["response"].startswith("Today:")
	assert learning_log