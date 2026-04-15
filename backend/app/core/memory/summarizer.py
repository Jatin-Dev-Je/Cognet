"""Memory Summarizer for Cognet.

Purpose:
Compress multiple memories into a concise summary.
"""

from __future__ import annotations

from app.infrastructure.ai.openai_client import client


def summarize_memories(memories: list[dict[str, object]]) -> str:
	"""Summarize a list of memory records into short structured text."""

	texts = [str(memory.get("content", "")) for memory in memories if memory.get("content")]
	if not texts:
		return "No long-term memory to summarize."

	prompt = f"""
Summarize the following user activity into key points:

{texts}

Keep it short and structured.
""".strip()

	response = client.chat.completions.create(
		model="gpt-4o-mini",
		messages=[{"role": "user", "content": prompt}],
	)

	return response.choices[0].message.content