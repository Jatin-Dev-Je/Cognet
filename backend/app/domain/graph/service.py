"""Graph Service for Cognet.

Purpose:
Store relationships between entities.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.core.identity import generate_id


GraphRecord = dict[str, Any]


@dataclass(slots=True)
class GraphService:
	"""Simple in-memory knowledge graph service."""

	storage: list[GraphRecord] = field(default_factory=list)

	def store_graph(self, user_id: str, entities: list[str], relations: list[tuple[str, str, str]]) -> GraphRecord:
		"""Store a graph record for a user."""

		record = {
			"id": generate_id(),
			"user_id": user_id,
			"entities": entities,
			"relations": relations,
			"version": 1,
			"is_deleted": False,
		}
		self.storage.append(record)
		return record

	def soft_delete_graph(self, graph_id: str) -> GraphRecord | None:
		record = next((item for item in self.storage if item.get("id") == graph_id), None)
		if record is None:
			return None
		record["is_deleted"] = True
		record["version"] = int(record.get("version", 1)) + 1
		return record