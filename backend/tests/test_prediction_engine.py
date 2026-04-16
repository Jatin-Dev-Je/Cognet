from __future__ import annotations

from app.core.inference.agent_runner import run_agents
from app.core.prediction.confidence import prediction_confidence
from app.core.prediction.pattern import detect_pattern
from app.core.prediction.predictor import predict_next
from app.core.prediction.proactive import run_prediction
from app.core.prediction.time_predictor import time_weighted_prediction
from app.domain.agent.service import AgentService


def test_pattern_detection_finds_progression() -> None:
	memories = [
		{"content": "API work"},
		{"content": "retrieval work"},
		{"content": "improve optimization"},
	]

	pattern = detect_pattern(memories)

	assert pattern == ["api", "retrieval", "optimization"]


def test_predictor_returns_expected_next_action() -> None:
	assert predict_next(["api"]) == "start retrieval system"
	assert predict_next(["retrieval"]) == "optimize retrieval accuracy"
	assert predict_next(["optimization"]) == "test system performance"


def test_prediction_confidence_scales_with_pattern_length() -> None:
	assert prediction_confidence(["api", "retrieval", "optimization"]) == 0.9
	assert prediction_confidence(["api", "retrieval"]) == 0.7
	assert prediction_confidence(["api"]) == 0.5


def test_time_weighted_prediction_uses_recent_items() -> None:
	memories = [
		{"content": "old api"},
		{"content": "older retrieval"},
		{"content": "improve optimization"},
	]

	assert time_weighted_prediction(memories) == ["api", "retrieval", "optimization"]


def test_proactive_engine_returns_prediction_payload() -> None:
	result = run_prediction([
		{"content": "API"},
		{"content": "retrieval"},
		{"content": "improve optimization"},
	])

	assert result["prediction"] in {"start retrieval system", "optimize retrieval accuracy", "test system performance", None}
	assert result["confidence"] >= 0.5


def test_agent_runner_adds_suggested_action_for_confident_prediction() -> None:
	context = {"tasks": ["Improve retrieval"]}
	results = run_agents(
		context,
		AgentService().agents,
		memories=[{"content": "API"}, {"content": "retrieval"}, {"content": "improve optimization"}],
	)

	assert any("Suggested next action:" in result for result in results)