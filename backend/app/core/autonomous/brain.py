"""Autonomous Brain for Cognet.

Purpose:
Decide actions without user input.

Inputs:
- memory
- prediction
- goals
- time

Output:
- action to execute
"""

from __future__ import annotations

from typing import Any, Mapping


def decide_autonomous_action(context: Mapping[str, Any], prediction: Mapping[str, Any]) -> dict[str, Any] | None:
	if float(prediction.get("confidence", 0)) > 0.8 and prediction.get("prediction"):
		return {
			"type": "suggest_next",
			"payload": prediction["prediction"],
		}

	if context.get("tasks"):
		return {
			"type": "remind",
			"payload": context["tasks"][0],
		}

	return None