"""Memory Entity with Temporal Awareness.

Purpose:
Add time intelligence to every memory.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any


def get_day_bucket(dt: datetime) -> str:
	now = datetime.utcnow()
	diff = (now - dt).days

	if diff == 0:
		return "today"
	if diff == 1:
		return "yesterday"
	if diff <= 7:
		return "this_week"
	return "older"


def enrich_temporal_memory(memory: dict[str, object], created_at: datetime | None = None) -> dict[str, object]:
	timestamp = created_at or datetime.utcnow()
	memory["created_at"] = timestamp
	memory["day_bucket"] = get_day_bucket(timestamp)
	memory["time_weight"] = 1.0 if memory["day_bucket"] == "today" else 0.8 if memory["day_bucket"] == "yesterday" else 0.6 if memory["day_bucket"] == "this_week" else 0.3
	return memory


def soft_delete_memory(memory: dict[str, Any]) -> dict[str, Any]:
	memory["is_deleted"] = True
	memory["version"] = int(memory.get("version", 1)) + 1
	return memory
