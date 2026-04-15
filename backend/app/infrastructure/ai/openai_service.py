"""OpenAI service wrapper for Cognet.

Purpose:
Build a strict, structured prompt for consistent chat responses.

Inputs:
- user_input: the current message from the user
- context: formatted structured context string
- response_generator: pluggable response function for local development

Output:
- str: generated assistant response

Steps:
- assemble a Cognet-specific prompt
- pass it to the response generator
- normalize the result
"""

from __future__ import annotations

from typing import Callable, Sequence

from app.core.context.formatter import clean_output


ResponseGenerator = Callable[[str], str]


def build_prompt(user_input: str, context: str, insights: Sequence[str] | None = None) -> str:
    """Build the prompt for Cognet responses."""

    insights_block = "\n".join(f"- {insight}" for insight in insights or [])
    if not insights_block:
        insights_block = "- None"

    return f"""
You are Cognet.

You think like a system, not a chatbot.

Context:
{context}

Insights:
{insights_block}

User: {user_input}

Instructions:
- Be concise
- Be structured
- Avoid generic phrases
- Do not say "based on context"
- Do not explain unnecessarily

Output format:
Current Focus:
...

Completed:
...

Next Steps:
...

Insight:
...
""".strip()


def generate_response(
    user_input: str,
    context: str,
    insights: Sequence[str] | None,
    response_generator: ResponseGenerator,
) -> str:
    """Generate a response using the Cognet prompt."""

    prompt = build_prompt(user_input, context, insights)
    return clean_output(response_generator(prompt))