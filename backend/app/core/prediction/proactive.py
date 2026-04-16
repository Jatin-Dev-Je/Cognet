"""Proactive Intelligence Engine for Cognet."""

from __future__ import annotations

from typing import Any, Sequence

from app.core.prediction.confidence import prediction_confidence
from app.core.prediction.pattern import detect_pattern
from app.core.prediction.predictor import predict_next
from app.core.prediction.time_predictor import time_weighted_prediction


def run_prediction(memories: Sequence[dict[str, Any]]) -> dict[str, Any]:
	pattern = detect_pattern(memories)
	recent_pattern = time_weighted_prediction(memories)
	if recent_pattern:
		pattern = recent_pattern

	next_step = predict_next(pattern)
	confidence = prediction_confidence(pattern)

	return {
		"prediction": next_step,
		"confidence": confidence,
		"pattern": pattern,
	}