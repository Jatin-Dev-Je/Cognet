"""MongoDB collections."""

from __future__ import annotations


memory_collection = "memory"
graph_collection = "knowledge_graph"


def ensure_indexes() -> dict[str, list[str]]:
	"""Return the intended indexes for core Mongo collections."""

	return {
		memory_collection: ["user_id", "session_id", "created_at"],
		graph_collection: ["user_id"],
	}
