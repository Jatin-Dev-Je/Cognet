from __future__ import annotations

from app.core.autonomous.brain import decide_autonomous_action
from app.core.autonomous.executor import execute_action
from app.core.autonomous.runner import run_autonomous
from app.core.autonomous.safety import is_safe
from app.core.autonomous.trigger import should_trigger
from app.core.intelligence.engine import IntelligenceEngine
from app.domain.agent.service import AgentService
from app.domain.goals.service import GoalService
from app.domain.graph.service import GraphService
from app.domain.memory.service import MemoryService
from app.domain.session.service import SessionService


def test_autonomous_trigger_uses_meaningful_memory() -> None:
	assert should_trigger({"type": "project"}) is True
	assert should_trigger({"type": "task"}) is True
	assert should_trigger({"type": "note"}) is False
	assert should_trigger(None) is False


def test_autonomous_brain_prefers_high_confidence_prediction() -> None:
	action = decide_autonomous_action({"tasks": ["Improve retrieval"]}, {"confidence": 0.9, "prediction": "start retrieval system"})

	assert action == {"type": "suggest_next", "payload": "start retrieval system"}


def test_autonomous_brain_falls_back_to_reminder() -> None:
	action = decide_autonomous_action({"tasks": ["Improve retrieval"]}, {"confidence": 0.2, "prediction": None})

	assert action == {"type": "remind", "payload": "Improve retrieval"}


def test_action_executor_formats_output() -> None:
	assert execute_action({"type": "suggest_next", "payload": "start retrieval system"}) == "Autonomous Suggestion: start retrieval system"
	assert execute_action({"type": "remind", "payload": "Improve retrieval"}) == "Reminder: Improve retrieval"
	assert execute_action(None) is None


def test_autonomous_safety_applies_cooldown(monkeypatch) -> None:
	times = iter([100.0, 110.0, 140.0])
	monkeypatch.setattr("app.core.autonomous.safety.time.time", lambda: next(times))

	assert is_safe("user-1") is True
	assert is_safe("user-1") is False
	assert is_safe("user-1") is True


def test_autonomous_runner_executes_suggestion() -> None:
	result = run_autonomous(
		"user-1",
		{"type": "project"},
		{"tasks": ["Improve retrieval"]},
		{"confidence": 0.9, "prediction": "start retrieval system"},
	)

	assert result == "Autonomous Suggestion: start retrieval system"


def test_engine_returns_autonomous_output() -> None:
	engine = IntelligenceEngine(
		memory_service=MemoryService(storage=[]),
		graph_service=GraphService(),
		agent_service=AgentService(),
		session_service=SessionService(),
		goal_service=GoalService(),
	)

	response = engine.run_intelligence("user-1", "I completed API", session_id="session-1")

	assert "autonomous_output" in response