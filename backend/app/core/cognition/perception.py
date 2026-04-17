"""Perception layer for Cognet."""

from __future__ import annotations

from app.core.inference.intent import detect_intent
from app.core.utils.sanitize import clean_input


def perceive_input(message: str) -> dict[str, str]:
	clean_text = clean_input(message)
	return {
		"clean_text": clean_text,
		"intent": detect_intent(clean_text),
	}