"""Intelligence Engine for Cognet.

Purpose:
Centralize memory, retrieval, agent, and response orchestration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter
from typing import Any, Callable

from app.core.context.builder import build_context, format_context
from app.core.embedding.engine import generate_embedding
from app.core.inference.agent_runner import run_agents
from app.core.inference.reasoning import generate_insights
from app.core.knowledge_graph.extractor import extract_entities
from app.core.memory.summarizer import summarize_memories
from app.core.retrieval.semantic import get_relevant_memories
from app.core.response.formatter import format_response
from app.config.settings import get_settings
from app.domain.agent.service import AgentService
from app.domain.goals.service import GoalService, extract_goal
from app.domain.graph.service import GraphService
from app.domain.memory.service import MemoryService
from app.domain.session.service import SessionService
from app.infrastructure.ai.openai_service import generate_response
from app.utils.logger import logger


ResponseGenerator = Callable[[str], str]


def default_response_generator(prompt: str) -> str:
	"""Fallback response generator used until the OpenAI layer is wired up."""

	return prompt


@dataclass(slots=True)
class IntelligenceEngine:
	"""Central intelligence orchestration for Cognet."""

	memory_service: MemoryService
	graph_service: GraphService = field(default_factory=GraphService)
	agent_service: AgentService = field(default_factory=AgentService)
	session_service: SessionService = field(default_factory=SessionService)
	goal_service: GoalService = field(default_factory=GoalService)
	response_generator: ResponseGenerator = default_response_generator

	def run_intelligence(
		self,
		user_id: str,
		message: str,
		session_id: str | None = None,
		top_k: int | None = None,
		memory_limit: int | None = None,
	) -> dict[str, Any]:
		"""Run the full Cognet intelligence pipeline."""

		settings = get_settings()
		top_k = top_k or settings.retrieval_top_k
		memory_limit = memory_limit or settings.max_context_memories
		started_at = perf_counter()
		logger.info("User: %s", message)

		try:
			query_embedding = generate_embedding(message)
			goal = extract_goal(message)
			session = self.session_service.update_session(user_id, session_id, active_project=goal, recent_action=message)
			memory = self.memory_service.save_memory(
				user_id,
				message,
				query_embedding,
				session_id=session.get("session_id"),
				goal=goal,
			)
			goal_record = self.goal_service.track_goal(user_id, goal, progress_item=message)
			graph_data = extract_entities(message)
			graph_record = self.graph_service.store_graph(user_id, graph_data["entities"], graph_data["relations"])
			all_memories = self.memory_service.get_recent_memories(user_id, limit=memory_limit, session_id=session.get("session_id"))
			long_term_memories = [memory_item for memory_item in all_memories if memory_item.get("memory_level") == "long"]
			short_term_memories = [memory_item for memory_item in all_memories if memory_item.get("memory_level") == "short"]
			long_term_summary = summarize_memories(long_term_memories[:20]) if len(long_term_memories) > 30 else None
			relevant_memories = get_relevant_memories(
				query_embedding=query_embedding,
				memories=short_term_memories + long_term_memories,
				top_k=top_k,
			)
			structured_context = build_context(relevant_memories)
			insights = generate_insights(structured_context)
			agent_outputs = run_agents(structured_context, self.agent_service.agents)
			formatted_context = format_context(structured_context)
			session_context = f"Session:\nactive_project: {session.get('active_project')}\nrecent_actions: {session.get('recent_actions', [])}"
			full_context = f"{session_context}\n\n{formatted_context}"
			if long_term_summary:
				full_context = f"{full_context}\n\nLong-Term Memory Summary:\n{long_term_summary}"
			if agent_outputs:
				full_context = f"{full_context}\n\nAgent Outputs:\n" + "\n".join(f"- {output}" for output in agent_outputs)

			logger.info("Context length: %s", len(full_context))
			response_text = generate_response(
				user_input=message,
				context=full_context,
				insights=insights,
				response_generator=self.response_generator,
			)
			primary_insight = insights[0] if insights else response_text
			response_time_ms = int((perf_counter() - started_at) * 1000)
			logger.info("Response time: %sms", response_time_ms)

			return {
				"user_id": user_id,
				"message": message,
				"session_id": session_id,
				"session": session,
				"saved_memory": memory,
				"goal": goal_record,
				"graph": graph_record,
				"long_term_summary": long_term_summary,
				"context": structured_context,
				"formatted_context": formatted_context,
				"agent_outputs": agent_outputs,
				"full_context": full_context,
				"insights": insights,
				"relevant_memories": relevant_memories,
				"response": format_response(
					{
						"project": structured_context.get("project"),
						"completed": structured_context.get("completed", []),
						"tasks": structured_context.get("tasks", []),
						"insight": primary_insight,
						"insights": insights,
						"raw_response": response_text,
					},
				),
				"raw_response": response_text,
				"response_time_ms": response_time_ms,
			}
		except Exception as exc:
			logger.error("Chat flow failed: %s", exc)
			return {
				"user_id": user_id,
				"message": message,
				"response": "System temporarily unavailable.",
				"error": str(exc),
			}