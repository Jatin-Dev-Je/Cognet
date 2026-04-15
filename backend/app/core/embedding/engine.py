"""Embedding Engine for Cognet.

Purpose:
Convert user text into a stable vector embedding for local development.

Inputs:
- text: the user message or memory content

Output:
- list[float]: normalized embedding vector

Steps:
- tokenize the text
- hash each token into a fixed-size vector
- normalize the vector length
"""

from __future__ import annotations

import hashlib
import re
from math import sqrt
from typing import Iterable


_EMBEDDING_CACHE: dict[tuple[str, int], list[float]] = {}


def _tokenize(text: str) -> list[str]:
	return re.findall(r"[a-z0-9]+", text.lower())


def _normalize(vector: list[float]) -> list[float]:
	magnitude = sqrt(sum(value * value for value in vector))
	if magnitude == 0:
		return vector
	return [value / magnitude for value in vector]


def generate_embedding(text: str, dimensions: int = 64) -> list[float]:
	"""Generate a deterministic embedding for a piece of text."""

	cache_key = (text, dimensions)
	if cache_key in _EMBEDDING_CACHE:
		return list(_EMBEDDING_CACHE[cache_key])

	vector = [0.0] * dimensions

	for token in _tokenize(text):
		digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
		index = int(digest, 16) % dimensions
		vector[index] += 1.0

	normalized = _normalize(vector)
	_EMBEDDING_CACHE[cache_key] = list(normalized)
	return normalized
