"""Learning layer for Cognet."""

from __future__ import annotations

from datetime import datetime
from typing import Any


learning_log: list[dict[str, Any]] = []


def learn(user_id: str, result: str) -> dict[str, Any]:
	entry = {
		"user_id": user_id,
		"result": result,
		"mode": "implicit",
		"created_at": datetime.utcnow(),
	}
	learning_log.append(entry)
	return entry