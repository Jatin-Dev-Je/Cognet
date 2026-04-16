"""Autonomous Runner for Cognet."""

from __future__ import annotations

from typing import Any, Mapping

from app.core.autonomous.brain import decide_autonomous_action
from app.core.autonomous.executor import execute_action
from app.core.autonomous.safety import is_safe
from app.core.autonomous.trigger import should_trigger


def run_autonomous(user_id: str, memory: Mapping[str, Any] | None, context: Mapping[str, Any], prediction: Mapping[str, Any]) -> str | None:
	if not should_trigger(memory):
		return None

	if not is_safe(user_id):
		return None

	action = decide_autonomous_action(context, prediction)
	result = execute_action(action)

	return result