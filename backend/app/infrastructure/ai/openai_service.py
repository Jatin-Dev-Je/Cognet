"""OpenAI service wrapper for Cognet."""

from __future__ import annotations

from typing import Callable, Sequence

from app.core.ai.llm import generate_response as _generate_response, generate_response_async as _generate_response_async
from app.core.ai.prompt import build_chat_prompt


ResponseGenerator = Callable[[str], str]


def build_prompt(user_input: str, context: str, insights: Sequence[str] | None = None) -> str:
	return build_chat_prompt(user_input, context, insights)


def generate_response(
	user_input: str,
	context: str,
	insights: Sequence[str] | None,
	response_generator: ResponseGenerator,
) -> str:
	return _generate_response(user_input, context, insights, response_generator)


async def generate_response_async(
	user_input: str,
	context: str,
	insights: Sequence[str] | None,
	response_generator: ResponseGenerator,
) -> str:
	return await _generate_response_async(user_input, context, insights, response_generator)