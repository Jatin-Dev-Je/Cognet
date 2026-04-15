"""Chat Use Case for Cognet.

Purpose:
Orchestrate the retrieval-aware chat flow.

Inputs:
- user_id: the active user identifier
- message: the current chat message
- memory_loader: callable that returns recent memories

Output:
- structured chat result with relevant memories, context, and a response

Steps:
- convert the message to an embedding
- load recent memories for the user
- retrieve the most relevant memories
- build a context string
- generate a response payload
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Sequence

from app.core.context.builder import build_context, format_context
from app.core.embedding.engine import generate_embedding
from app.core.inference.reasoning import generate_insights
from app.core.retrieval.semantic import get_relevant_memories
from app.infrastructure.ai.openai_service import generate_response


MemoryDocument = dict[str, Any]
MemoryLoader = Callable[[str, int], Sequence[MemoryDocument]]
ResponseGenerator = Callable[[str], str]


def default_response_generator(prompt: str) -> str:
	"""Fallback response generator used until the OpenAI layer is wired up."""

	return prompt


def get_recent_memories(
	user_id: str,
	limit: int = 50,
	memory_loader: MemoryLoader | None = None,
) -> list[MemoryDocument]:
	"""Load the latest memories for a user through the injected loader."""

	if memory_loader is None:
		return []

	return list(memory_loader(user_id, limit))


@dataclass(slots=True)
class ChatUseCase:
	"""Chat orchestration focused on relevant memory retrieval."""

	memory_loader: MemoryLoader
	response_generator: ResponseGenerator = default_response_generator

	def handle_chat(
		self,
		user_id: str,
		message: str,
		top_k: int = 5,
		memory_limit: int = 50,
	) -> dict[str, Any]:
		query_embedding = generate_embedding(message)
		all_memories = get_recent_memories(user_id, limit=memory_limit, memory_loader=self.memory_loader)
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
