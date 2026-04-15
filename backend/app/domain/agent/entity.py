"""Agent Entity for Cognet.

Purpose:
Represent a task automation rule.

Fields:
- name
- trigger_type
- condition
- action
- active
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping


Context = Mapping[str, Any]
Condition = Callable[[Context], bool]
Action = Callable[[Context], str]


@dataclass(slots=True)
class Agent:
	"""Simple rule-based agent."""

	name: str
	trigger_type: str
	condition: Condition
	action: Action
	active: bool = True
