from __future__ import annotations

from app.core.agents.orchestrator import run_agents
from app.core.intelligence.engine import IntelligenceEngine
from app.domain.agent.service import AgentService
from app.domain.goals.service import GoalService
from app.domain.graph.service import GraphService
from app.domain.memory.service import MemoryService
from app.domain.session.service import SessionService


def test_multi_agent_orchestrator_builds_response() -> None:
	response = run_agents(
		{
			"intent": "ask_next_step",
			"tasks": ["improving retrieval accuracy"],
			"completed": ["API"],
			"temporal": {"today": ["working on retrieval"], "yesterday": [], "this_week": []},
			"prediction": {"prediction": "start retrieval system", "confidence": 0.9},
		}
	)

	assert "Today:" in response
	assert "Completed:" in response
	assert "Next Step:" in response
	assert "Insight:" in response
	assert "Focus on improving retrieval accuracy" in response or "Focus on improving retrieval accuracy" in response.replace("-", "")


def test_engine_exposes_multi_agent_output() -> None:
	engine = IntelligenceEngine(
		memory_service=MemoryService(storage=[]),
		graph_service=GraphService(),
		agent_service=AgentService(),
		session_service=SessionService(),
		goal_service=GoalService(),
	)

	result = engine.run_intelligence("user-1", "I completed API and what should I do next?", session_id="session-1")

	assert result["multi_agent_output"]
	assert result["response"] == result["final_output"]