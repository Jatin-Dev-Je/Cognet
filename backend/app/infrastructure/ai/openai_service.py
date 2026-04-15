"""OpenAI service wrapper for Cognet.

Purpose:
Build a structured prompt for intelligent chat responses.

Inputs:
- user_input: the current message from the user
- context: formatted structured context string
- response_generator: pluggable response function for local development

Output:
- str: generated assistant response

Steps:
- assemble a Cognet-specific prompt
- pass it to the response generator
- return the generated response
"""

from __future__ import annotations

from typing import Callable, Sequence


ResponseGenerator = Callable[[str], str]


def build_prompt(user_input: str, context: str, insights: Sequence[str] | None = None) -> str:
    """Build the prompt for Cognet responses."""

    insights_block = "\n".join(f"- {insight}" for insight in insights or [])
    if not insights_block:
        insights_block = "- None"

    return f"""
You are Cognet, a system that deeply understands the user.

You do NOT behave like a chatbot.
You behave like an intelligent system that remembers, understands, and guides.

Context:
{context}

Insights:
{insights_block}

User: {user_input}

Instructions:
- Be concise but intelligent
- Show awareness of past work
- Suggest next steps naturally
- Do NOT sound generic
- Do NOT say "based on context"
- Speak like you already know the user

Output format:
- What user is doing
- What is done
- What is next
- Optional insight
""".strip()


def generate_response(
    user_input: str,
    context: str,
    insights: Sequence[str] | None,
    response_generator: ResponseGenerator,
) -> str:
    """Generate a response using the Cognet prompt."""

    prompt = build_prompt(user_input, context, insights)
    return response_generator(prompt)