"""Chat Use Case Flow for Cognet."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

from app.core.ai.embedding import generate_embedding_async
from app.core.jobs.worker import run_background
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

	async def handle_chat_async(
		self,
		user_id: str,
		message: str,
		session_id: str | None = None,
		top_k: int = 5,
		memory_limit: int = 30,
	) -> dict[str, Any]:
		result = await self.intelligence_engine.run_intelligence_async(
			user_id,
			message,
			session_id=session_id,
			top_k=top_k,
			memory_limit=memory_limit,
		)
		if session_id is not None:
			run_background(self._persist_background_summary(user_id, message, session_id, result))
		return result

	async def _persist_background_summary(
		self,
		user_id: str,
		message: str,
		session_id: str,
		result: dict[str, Any],
	) -> None:
		background_summary = f"Assistant response summary: {str(result.get('response', ''))[:500]}"
		embedding = await generate_embedding_async(background_summary or message)
		await self.memory_service.save_memory_async(
			user_id,
			background_summary,
			embedding,
			session_id=session_id,
			goal=str(result.get("goal", "")) or None,
		)
