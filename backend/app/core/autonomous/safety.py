"""Safety layer for Cognet autonomous mode."""

from __future__ import annotations

import time
from typing import Final


_last_action_time: dict[str, float] = {}
_cooldown_seconds: Final[int] = 30


def is_safe(user_id: str) -> bool:
	now = time.time()

	if user_id not in _last_action_time:
		_last_action_time[user_id] = now
		return True

	if now - _last_action_time[user_id] < _cooldown_seconds:
		return False

	_last_action_time[user_id] = now
	return True