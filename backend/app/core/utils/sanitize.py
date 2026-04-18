"""Input sanitization helpers for Cognet."""

from __future__ import annotations


def clean_input(text: str) -> str:
	"""
	Clean and truncate input text to a maximum of 1000 characters.
	Args:
		text (str): The input string to sanitize.
	Returns:
		str: The sanitized and truncated string.
	"""
	return text.strip()[:1000]