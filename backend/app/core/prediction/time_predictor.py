"""Time-aware prediction helpers for Cognet."""

from __future__ import annotations

from typing import Any, Sequence

from app.core.prediction.pattern import detect_pattern


def time_weighted_prediction(memories: Sequence[dict[str, Any]]) -> list[str]:
	recent = memories[-3:]
	return detect_pattern(recent)