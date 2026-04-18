"""OpenAI service wrapper for Cognet."""

from __future__ import annotations

from typing import Callable, Sequence

from app.core.context.formatter import clean_output
from app.core.ai.prompt import build_chat_prompt


ResponseGenerator = Callable[[str], str]


def build_temporal_prompt(



def generate_response(
	user_input: str,
	context: str,
	insights: Sequence[str] | None,
	response_generator: ResponseGenerator,
	temporal_context: str | None = None,
	next_step: str | None = None,
) -> str:
	prompt = build_chat_prompt(user_input, context, insights, temporal_context=temporal_context, next_step=next_step)
	return clean_output(response_generator(prompt))


async def generate_response_async(
	user_input: str,
	context: str,
	insights: Sequence[str] | None,
	response_generator: ResponseGenerator,
	temporal_context: str | None = None,
	next_step: str | None = None,
) -> str:
	prompt = build_chat_prompt(user_input, context, insights, temporal_context=temporal_context, next_step=next_step)
	return clean_output(response_generator(prompt))


def generate_temporal_response(
	user_input: str,
	context: str,
	insights: Sequence[str] | None,
	temporal_context: str | None,
	next_step: str | None,
	response_generator: ResponseGenerator,
) -> str:
	return generate_response(user_input, context, insights, response_generator, temporal_context=temporal_context, next_step=next_step)