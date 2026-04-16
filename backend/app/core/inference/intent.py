"""Intent Detection Engine for Cognet."""

from __future__ import annotations


def detect_intent(text: str) -> str:
	text = text.lower()

	if "what should i do" in text or "next" in text:
		return "ask_next_step"

	if "what am i doing" in text or "status" in text:
		return "ask_status"

	if "completed" in text or "done" in text:
		return "update_progress"

	if "i want to" in text or "i will" in text:
		return "new_goal"

	return "general"