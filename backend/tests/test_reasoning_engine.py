from __future__ import annotations

from app.core.context.final_formatter import format_final
from app.core.reasoning.chain import build_memory_chain
from app.core.reasoning.engine import reason_over_chain
from app.core.reasoning.expand import expand_context
from app.core.reasoning.graph import build_reasoning_graph
from app.core.reasoning.insight import generate_insight
from app.core.reasoning.order import sort_chain
from app.core.intelligence.engine import IntelligenceEngine
from app.domain.agent.service import AgentService
from app.domain.goals.service import GoalService
from app.domain.graph.service import GraphService
from app.domain.memory.service import MemoryService
from app.domain.session.service import SessionService


def test_memory_chain_builder_and_ordering() -> None:
	memories = [
		{"content": "I am optimizing performance"},
		{"content": "I completed API"},
		{"content": "I worked on retrieval"},
	]

	chain = build_memory_chain(memories)
	ordered_chain = sort_chain(chain)

	assert [step for step, _ in ordered_chain] == ["api", "retrieval", "optimization"]


def test_reasoning_graph_and_insight_are_generated() -> None:
	chain = [
		("api", {"content": "I completed API"}),
		("retrieval", {"content": "I worked on retrieval"}),
		("optimization", {"content": "I am optimizing performance"}),
	]

	assert reason_over_chain(chain) == "You moved from API development to retrieval and are now optimizing it"
	assert expand_context(chain) == ["I completed API", "I worked on retrieval", "I am optimizing performance"]
	assert build_reasoning_graph(chain) == {
		"nodes": ["api", "retrieval", "optimization"],
		"edges": ["api -> retrieval", "retrieval -> optimization"],
	}
	assert generate_insight(chain) == "You are following a complete backend development lifecycle"


def test_final_formatter_includes_reasoning_and_insight() -> None:
	formatted = format_final(
		{"temporal": {"today": ["optimizing performance"], "yesterday": [], "this_week": []}, "recent": [], "completed": ["API"]},
		"Focus on improving retrieval accuracy",
		reasoning="You moved from API development to retrieval and are now optimizing it",
		insight="You are following a complete backend development lifecycle",
	)

	assert "Reasoning:" in formatted
	assert "Insight:" in formatted
	assert "Completed:" in formatted


def test_engine_uses_memory_driven_reasoning_across_steps() -> None:
	engine = IntelligenceEngine(
		memory_service=MemoryService(storage=[]),
		graph_service=GraphService(),
		agent_service=AgentService(),
		session_service=SessionService(),
		goal_service=GoalService(),
	)

	engine.run_intelligence("user-1", "I completed API", session_id="session-1")
	engine.run_intelligence("user-1", "I worked on retrieval", session_id="session-1")
	result = engine.run_intelligence("user-1", "I am optimizing performance", session_id="session-1")

	assert "Reasoning:" in result["response"]
	assert "Insight:" in result["response"]
	assert result["reasoning"]
	assert result["insight"]
	assert result["agent_state"] in {"stable", "switch_strategy"}