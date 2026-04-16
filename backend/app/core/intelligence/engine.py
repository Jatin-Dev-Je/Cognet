"""Intelligence Engine for Cognet.

Purpose:
Centralize memory, retrieval, agent, and response orchestration.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from time import perf_counter
from typing import Any, Callable

from app.core.context.builder import build_context, format_context
from app.core.context.final_formatter import format_final
from app.core.context.formatter import format_temporal_context
from app.core.context.temporal_builder import group_by_time
from app.core.embedding.engine import generate_embedding
from app.core.ai.prompt import PROMPT_VERSION
from app.core.config.flags import FEATURES
from app.core.inference.agent_runner import run_agents
from app.core.inference.decision import decide_action
from app.core.inference.fusion import fuse_context
from app.core.inference.intent import detect_intent
from app.core.inference.reasoning import generate_insights
from app.core.inference.next_step import suggest_next
from app.core.prediction.proactive import run_prediction
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
from app.infrastructure.ai.openai_service import build_temporal_prompt
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

	async def run_intelligence_async(
		self,
		user_id: str,
		message: str,
		session_id: str | None = None,
		top_k: int | None = None,
		memory_limit: int | None = None,
	) -> dict[str, Any]:
		return await asyncio.to_thread(
			self.run_intelligence,
			user_id,
			message,
			session_id,
			top_k,
			memory_limit,
		)

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
			recent_memories = [memory_item for memory_item in all_memories if not memory_item.get("is_deleted")]
			long_term_memories = [memory_item for memory_item in recent_memories if memory_item.get("memory_level") == "long"]
			short_term_memories = [memory_item for memory_item in recent_memories if memory_item.get("memory_level") == "short"]
			long_term_summary = summarize_memories(long_term_memories[:20]) if FEATURES.get("summarization", True) and len(long_term_memories) > 30 else None
			relevant_memories = get_relevant_memories(
				query_embedding=query_embedding,
				memories=short_term_memories + long_term_memories,
				top_k=top_k,
			)
			structured_context = build_context(relevant_memories)
			insights = generate_insights(structured_context)
			intent = detect_intent(message)
			temporal_context = group_by_time(relevant_memories)
			fused = fuse_context(intent, temporal_context, structured_context)
			decision = decide_action(fused)
			next_step = suggest_next(structured_context)
			prediction = run_prediction(relevant_memories)
			agent_outputs = run_agents(structured_context, self.agent_service.agents, memories=relevant_memories) if FEATURES.get("agents", True) else []
			formatted_context = format_context(structured_context)
			temporal_context_text = format_temporal_context(temporal_context)
			session_context = f"Session:\nactive_project: {session.get('active_project')}\nrecent_actions: {session.get('recent_actions', [])}"
			full_context = f"{session_context}\n\n{formatted_context}"
			if long_term_summary:
				full_context = f"{full_context}\n\nLong-Term Memory Summary:\n{long_term_summary}"
			if agent_outputs:
				full_context = f"{full_context}\n\nAgent Outputs:\n" + "\n".join(f"- {output}" for output in agent_outputs)

			logger.info("Context length: %s", len(full_context))
			prediction_text = None
			if prediction.get("prediction") and prediction.get("confidence", 0) > 0.7:
				prediction_text = f"You will likely {prediction['prediction']} next"
			final_output = format_final(fused, decision, prediction=prediction_text)
			response_text = final_output
			prompt_preview = build_temporal_prompt(
				user_input=message,
				context=full_context,
				insights=insights,
				temporal_context=temporal_context_text,
				next_step=decision,
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
				"intent": intent,
				"fused": fused,
				"decision": decision,
				"formatted_context": formatted_context,
				"agent_outputs": agent_outputs,
				"full_context": full_context,
				"temporal_context": temporal_context_text,
				"next_step": next_step,
				"prediction": prediction,
				"final_output": final_output,
				"prompt_preview": prompt_preview,
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
						"temporal_context": temporal_context_text,
						"next_step": next_step,
						"prediction": prediction_text,
						"prompt_version": PROMPT_VERSION,
					},
				),
				"raw_response": response_text,
				"response_time_ms": response_time_ms,
				"prompt_version": PROMPT_VERSION,
				"trace": {
					"memories_used": len(relevant_memories),
					"agents_triggered": len(agent_outputs),
					"prediction_confidence": prediction.get("confidence", 0),
					"latency_ms": response_time_ms,
				},
			}
		except Exception as exc:
			logger.error("Chat flow failed: %s", exc)
			return {
				"user_id": user_id,
				"message": message,
				"response": "System temporarily unavailable.",
				"error": str(exc),
				"prompt_version": PROMPT_VERSION,
				"trace": {"memories_used": 0, "agents_triggered": 0, "prediction_confidence": 0, "latency_ms": int((perf_counter() - started_at) * 1000)},
			}