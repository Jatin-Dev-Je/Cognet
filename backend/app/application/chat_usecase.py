"""Chat Use Case Flow for Cognet.

Purpose:
Save memory, retrieve relevant memories, build structured context, and generate a guided response.

Steps:
1. generate embedding
2. save memory
3. fetch memories
4. run hybrid retrieval
5. build structured context
6. format context
7. call LLM
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from app.core.context.builder import build_context, format_context
from app.core.embedding.engine import generate_embedding
from app.core.inference.reasoning import generate_insights
from app.core.retrieval.semantic import get_relevant_memories
from app.domain.memory.service import MemoryService
from app.infrastructure.ai.openai_service import generate_response


MemoryDocument = dict[str, Any]
ResponseGenerator = Callable[[str], str]


def default_response_generator(prompt: str) -> str:
	"""Fallback response generator used until the OpenAI layer is wired up."""

	return prompt


@dataclass(slots=True)
class ChatUseCase:
	"""Chat orchestration focused on relevant memory retrieval."""

	memory_service: MemoryService
	response_generator: ResponseGenerator = default_response_generator

	def handle_chat(
		self,
		user_id: str,
		message: str,
		top_k: int = 5,
		memory_limit: int = 50,
	) -> dict[str, Any]:
		query_embedding = generate_embedding(message)
		self.memory_service.save_memory(user_id, message, query_embedding)
		all_memories = self.memory_service.get_recent_memories(user_id, limit=memory_limit)
		relevant_memories = get_relevant_memories(
			query_embedding=query_embedding,
			memories=all_memories,
			top_k=top_k,
		)
		structured_context = build_context(relevant_memories)
		insights = generate_insights(structured_context)
		formatted_context = format_context(structured_context)
		response = generate_response(
			user_input=message,
			context=formatted_context,
			insights=insights,
			response_generator=self.response_generator,
		)

		return {
			"user_id": user_id,
			"message": message,
			"context": structured_context,
			"formatted_context": formatted_context,
			"insights": insights,
			"relevant_memories": relevant_memories,
			"response": response,
		}
