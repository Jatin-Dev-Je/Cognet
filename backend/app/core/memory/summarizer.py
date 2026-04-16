"""Memory Summarizer for Cognet."""

from __future__ import annotations

import asyncio

from app.core.ai.prompt import build_summary_prompt
from app.infrastructure.ai.openai_client import client


def summarize_memories(memories: list[dict[str, object]]) -> str:
	"""Summarize a list of memory records into short structured text."""

	texts = [str(memory.get("content", "")) for memory in memories if memory.get("content")]
	if not texts:
		return "No long-term memory to summarize."

	prompt = build_summary_prompt(texts)
	response = client.chat.completions.create(
		model="gpt-4o-mini",
		messages=[{"role": "user", "content": prompt}],
	)

	return str(response.choices[0].message.content)


async def summarize_memories_async(memories: list[dict[str, object]]) -> str:
	return await asyncio.to_thread(summarize_memories, memories)