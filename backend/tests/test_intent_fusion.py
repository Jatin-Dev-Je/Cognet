from __future__ import annotations

from app.application.chat_usecase import ChatUseCase
from app.core.context.final_formatter import format_final
from app.core.context.temporal_builder import group_by_time
from app.core.inference.decision import decide_action
from app.core.inference.fusion import fuse_context
from app.core.inference.intent import detect_intent
from app.domain.agent.service import AgentService
from app.domain.graph.service import GraphService
from app.domain.goals.service import GoalService
from app.domain.memory.service import MemoryService
from app.domain.session.service import SessionService


def test_detect_intent_maps_common_phrases() -> None:
	assert detect_intent("What should I do next?") == "ask_next_step"
	assert detect_intent("What is my status?") == "ask_status"
	assert detect_intent("I completed the API") == "update_progress"
	assert detect_intent("I want to build Cognet") == "new_goal"


def test_fusion_and_decision_produce_next_step() -> None:
	structured = {"tasks": ["improve retrieval"], "completed": ["API"], "project": "Cognet"}
	temporal = {"today": ["working on retrieval"], "yesterday": ["completed API"], "this_week": []}
	fused = fuse_context("ask_next_step", temporal, structured)
	decision = decide_action(fused)
	formatted = format_final(fused, decision)

	assert decision == "Focus on: improve retrieval"
	assert "Today:" in formatted
	assert "Yesterday:" in formatted
	assert "Next Step:" in formatted


def test_chat_use_case_includes_intent_and_decision() -> None:
	memory_service = MemoryService(storage=[])
	service = ChatUseCase(
		memory_service=memory_service,
		graph_service=GraphService(),
		agent_service=AgentService(),
		session_service=SessionService(),
		goal_service=GoalService(),
	)

	result = service.handle_chat("user-1", "I completed API yesterday and what should I do next?", session_id="session-1")

	assert result["intent"] == "ask_next_step"
	assert result["decision"]
	assert "Next Step:" in result["response"]


def test_grouped_temporal_context_is_used() -> None:
	memories = [
		{"content": "Today work", "day_bucket": "today"},
		{"content": "Yesterday work", "day_bucket": "yesterday"},
	]
	grouped = group_by_time(memories)

	assert grouped["today"] == ["Today work"]
	assert grouped["yesterday"] == ["Yesterday work"]