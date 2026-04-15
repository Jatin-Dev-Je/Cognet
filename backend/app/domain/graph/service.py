"""Graph Service for Cognet.

Purpose:
Store relationships between entities.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


GraphRecord = dict[str, Any]


@dataclass(slots=True)
class GraphService:
	"""Simple in-memory knowledge graph service."""

	storage: list[GraphRecord] = field(default_factory=list)

	def store_graph(self, user_id: str, entities: list[str], relations: list[tuple[str, str, str]]) -> GraphRecord:
		"""Store a graph record for a user."""

		record = {
			"user_id": user_id,
			"entities": entities,
			"relations": relations,
		}
		self.storage.append(record)
		return record