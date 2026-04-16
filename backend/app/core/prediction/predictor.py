"""Next Action Predictor for Cognet."""

from __future__ import annotations


def predict_next(pattern: list[str]) -> str | None:
	if pattern[-1:] == ["api"]:
		return "start retrieval system"

	if pattern[-1:] == ["retrieval"]:
		return "optimize retrieval accuracy"

	if pattern[-1:] == ["optimization"]:
		return "test system performance"

	return None