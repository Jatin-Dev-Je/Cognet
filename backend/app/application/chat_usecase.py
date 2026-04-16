"""Chat Use Case Flow for Cognet."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.core.intelligence.engine import IntelligenceEngine
from app.domain.agent.service import AgentService
from app.domain.graph.service import GraphService
from app.domain.goals.service import GoalService
from app.domain.memory.service import MemoryService
from app.domain.session.service import SessionService
from app.utils.logger import logger


@dataclass(slots=True)
class ChatUseCase:
	"""Thin chat facade over the intelligence engine."""

	memory_service: MemoryService
	graph_service: GraphService | None = None
	agent_service: AgentService | None = None
	session_service: SessionService | None = None
	goal_service: GoalService | None = None
	intelligence_engine: IntelligenceEngine | None = None

	def __post_init__(self) -> None:
		if self.intelligence_engine is None:
			self.intelligence_engine = IntelligenceEngine(
				memory_service=self.memory_service,
				graph_service=self.graph_service or GraphService(),
				agent_service=self.agent_service or AgentService(),
				session_service=self.session_service or SessionService(),
				goal_service=self.goal_service or GoalService(),
			)

	def handle_chat(
		self,
		user_id: str,
		message: str,
		session_id: str | None = None,
		top_k: int = 5,
		memory_limit: int = 30,
	) -> dict[str, Any]:
		logger.info("User input: %s", message)
		result = self.intelligence_engine.run_intelligence(
			user_id,
			message,
			session_id=session_id,
			top_k=top_k,
			memory_limit=memory_limit,
		)
		logger.info("Retrieved memories: %s", len(result.get("relevant_memories", [])))
		logger.info("Response time: %sms", result.get("response_time_ms", 0))
		return result
