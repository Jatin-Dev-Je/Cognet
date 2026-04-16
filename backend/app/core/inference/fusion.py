"""Intent + Time Fusion Engine for Cognet."""

from __future__ import annotations

from typing import Any, Mapping


def fuse_context(intent: str, temporal_data: Mapping[str, list[str]], structured_context: Mapping[str, Any]) -> dict[str, Any]:
	result: dict[str, Any] = {}
	result["recent"] = temporal_data.get("today", [])
	result["intent"] = intent
	result["tasks"] = list(structured_context.get("tasks", []))
	result["completed"] = list(structured_context.get("completed", []))
	result["temporal"] = dict(temporal_data)
	result["project"] = structured_context.get("project")
	return result