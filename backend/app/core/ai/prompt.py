"""Prompt templates for Cognet AI."""

from __future__ import annotations

from typing import Sequence


def build_chat_prompt(user_input: str, context: str, insights: Sequence[str] | None = None) -> str:
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


def build_summary_prompt(texts: Sequence[str]) -> str:
	joined_text = "\n".join(f"- {text}" for text in texts) or "- No meaningful activity found."
	return f"""
Summarize the following user activity into key points:

{joined_text}

Keep it short and structured.
""".strip()