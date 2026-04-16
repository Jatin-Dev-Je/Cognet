"""Input sanitization helpers for Cognet."""

from __future__ import annotations


def clean_input(text: str) -> str:
	return text.strip()[:1000]