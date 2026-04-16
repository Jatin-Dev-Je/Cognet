"""Prompt templates for Cognet AI."""

from __future__ import annotations

from typing import Sequence


PROMPT_VERSION = "v1"


def build_chat_prompt(
	user_input: str,
	context: str,
	insights: Sequence[str] | None = None,
	temporal_context: str | None = None,
	next_step: str | None = None,
) -> str:
	insights_block = "\n".join(f"- {insight}" for insight in insights or [])
	if not insights_block:
		insights_block = "- None"
	temporal_block = temporal_context or "- None"
	next_step_block = next_step or "Define your next goal"

	return f"""
You are Cognet.

You understand user work across time.

Context:
{context}

Temporal Context:
{temporal_block}

Insights:
{insights_block}

Next Step:
{next_step_block}

User: {user_input}

Instructions:
- Be concise
- Be structured
- Avoid generic phrases
- Do not say "based on context"
- Do not explain unnecessarily
- prioritize recent work
- suggest the next logical step

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


def build_summary_prompt(texts: Sequence[str]) -> str:
	joined_text = "\n".join(f"- {text}" for text in texts) or "- No meaningful activity found."
	return f"""
Summarize the following user activity into key points:

{joined_text}

Keep it short and structured.
""".strip()