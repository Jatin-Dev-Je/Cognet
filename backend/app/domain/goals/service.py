"""Goal Tracker for Cognet.

Purpose:
Extract and track user goals from input and memory.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


GoalRecord = dict[str, Any]


def extract_goal(text: str) -> str | None:
	"""Extract a goal from user input."""

	content = text.lower()
	if "build" in content or "create" in content or "finish" in content:
		return text.strip()
	return None


@dataclass(slots=True)
class GoalService:
	"""In-memory goal tracker."""

	storage: list[GoalRecord] = field(default_factory=list)

	def track_goal(self, user_id: str, goal: str | None, progress_item: str | None = None) -> GoalRecord | None:
		"""Store or update a goal record."""

		if goal is None:
			return None

		record = next((item for item in self.storage if item.get("user_id") == user_id and item.get("goal") == goal), None)
		if record is None:
			record = {"user_id": user_id, "goal": goal, "progress": []}
			self.storage.append(record)
		if progress_item and progress_item not in record["progress"]:
			record["progress"].append(progress_item)
		return record

	def get_goal(self, user_id: str) -> GoalRecord | None:
		"""Return the latest goal for a user."""

		for record in reversed(self.storage):
			if record.get("user_id") == user_id:
				return record
		return None