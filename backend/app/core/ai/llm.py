"""
LLM pipeline for Cognet.

Purpose:
- Provide synchronous and asynchronous interfaces for generating responses and summaries using LLMs.
- Standardize prompt construction and output cleaning for downstream consumers.

Inputs:
- user_input: User's message or query.
- context: Relevant context string for the LLM.
- insights: Optional list of insight strings to enrich the prompt.
- response_generator: Callable that takes a prompt and returns a string response (e.g., OpenAI API call).

Outputs:
- Cleaned LLM response or summary string.
"""

from __future__ import annotations

import asyncio
from typing import Callable, Sequence

from app.core.context.formatter import clean_output
from app.core.ai.prompt import build_chat_prompt, build_summary_prompt


ResponseGenerator = Callable[[str], str]


def generate_response(
	user_input: str,
	context: str,
	insights: Sequence[str] | None,
	response_generator: ResponseGenerator,
) -> str:
	prompt = build_chat_prompt(user_input, context, insights)
	return clean_output(response_generator(prompt))


async def generate_response_async(
	user_input: str,
	context: str,
	insights: Sequence[str] | None,
	response_generator: ResponseGenerator,
) -> str:
	return await asyncio.to_thread(generate_response, user_input, context, insights, response_generator)


def summarize_text(texts: Sequence[str], response_generator: ResponseGenerator) -> str:
	prompt = build_summary_prompt(texts)
	return clean_output(response_generator(prompt))


async def summarize_text_async(texts: Sequence[str], response_generator: ResponseGenerator) -> str:
	return await asyncio.to_thread(summarize_text, texts, response_generator)