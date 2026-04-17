"""Planning layer for Cognet."""

from __future__ import annotations

from typing import Any, Mapping


def plan(context: Mapping[str, Any], prediction: Mapping[str, Any] | None = None) -> str:
	prediction = dict(prediction or {})
	if prediction.get("prediction") and float(prediction.get("confidence", 0)) > 0.8:
		return str(prediction["prediction"])

	tasks = list(context.get("tasks", []))
	if tasks:
		return str(tasks[0])

	return "Define next goal"