from app.application.chat_usecase import ChatUseCase
from app.core.embedding.engine import generate_embedding
from app.core.memory.summarizer import summarize_memories
from app.domain.agent.service import AgentService
from app.domain.graph.service import GraphService
from app.domain.memory.service import MemoryService
from app.domain.session.service import SessionService
from app.domain.goals.service import GoalService, extract_goal


def test_goal_extraction_returns_goal_text() -> None:
	assert extract_goal("I want to build Cognet backend") == "I want to build Cognet backend"


def test_session_service_tracks_state() -> None:
	service = SessionService()
	session = service.update_session("user-1", "session-1", active_project="Cognet backend", recent_action="Started work")

	assert session["active_project"] == "Cognet backend"
	assert session["recent_actions"] == ["Started work"]


def test_summarizer_returns_short_summary() -> None:
	result = summarize_memories([
		{"content": "Built API setup"},
		{"content": "Improved retrieval"},
	])

	assert result


def test_chat_use_case_emits_session_and_goal() -> None:
	memory_service = MemoryService(storage=[])
	chat = ChatUseCase(
		memory_service=memory_service,
		graph_service=GraphService(),
		agent_service=AgentService(),
		session_service=SessionService(),
		goal_service=GoalService(),
	)

	result = chat.handle_chat("user-1", "I am building Cognet backend", session_id="session-1")

	assert result["session"]["active_project"] is not None
	assert result["saved_memory"]["memory_level"] in {"short", "long"}


def test_chat_use_case_async_wrapper_returns_result() -> None:
	memory_service = MemoryService(storage=[])
	chat = ChatUseCase(
		memory_service=memory_service,
		graph_service=GraphService(),
		agent_service=AgentService(),
		session_service=SessionService(),
		goal_service=GoalService(),
	)

	import asyncio

	result = asyncio.run(chat.handle_chat_async("user-1", "I am building Cognet backend", session_id="session-1"))

	assert result["session"]["active_project"] is not None