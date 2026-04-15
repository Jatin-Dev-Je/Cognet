"""Context formatter for Cognet."""

from __future__ import annotations


def clean_output(text: str) -> str:
	"""Trim generated text for stable output."""

	return text.strip()