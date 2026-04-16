"""Knowledge Graph Extractor for Cognet.

Purpose:
Extract entities and relationships from user input.

Output:
{
  entities: ["Cognet", "backend"],
  relations: [("user", "working_on", "Cognet")]
}
"""

from __future__ import annotations

import re
from typing import Iterable


TECH_TERMS = {"backend", "api", "memory", "retrieval", "context", "graph", "openai", "mongodb"}


def extract_entities(text: str) -> dict[str, list[tuple[str, str, str]] | list[str]]:
	"""Extract simple entities and relations from text."""

	tokens = re.findall(r"[A-Za-z0-9_]+", text)
	entities: list[str] = []
	relations: list[tuple[str, str, str]] = []

	for token in tokens:
		lowered = token.lower()
		if token[:1].isupper() or lowered in TECH_TERMS:
			entities.append(token)

	if entities:
		target = next((entity for entity in entities if entity != "I"), entities[0])
		relations.append(("user", "working_on", target))

	return {"entities": entities, "relations": relations}