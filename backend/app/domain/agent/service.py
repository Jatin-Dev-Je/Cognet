"""Agent Service for Cognet.

Purpose:
Evaluate agents against current context and trigger actions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from app.domain.agent.entity import Agent


Context = Mapping[str, Any]


def task_reminder_condition(context: Context) -> bool:
	"""Trigger when there are pending tasks."""

	return len(context.get("tasks", [])) > 0


def task_reminder_action(context: Context) -> str:
	"""Return a short task reminder."""

	return f"You have pending tasks: {context['tasks'][0]}"


def focus_agent_condition(context: Context) -> bool:
	"""Trigger when there are multiple pending tasks."""

	return len(context.get("tasks", [])) > 2


def focus_agent_action(context: Context) -> str:
	"""Return a focus suggestion."""

	return "You have multiple tasks. Focus on one to make progress."


def build_default_agents() -> list[Agent]:
	"""Create the default Cognet agents."""

	return [
		Agent(
			name="task_reminder",
			trigger_type="context",
			condition=task_reminder_condition,
			action=task_reminder_action,
		),
		Agent(
			name="focus_suggestion",
			trigger_type="context",
			condition=focus_agent_condition,
			action=focus_agent_action,
		),
	]


def evaluate_agents(context: Context, agents: Sequence[Agent]) -> list[str]:
	"""Evaluate all active agents against a context."""

	triggered: list[str] = []

	for agent in agents:
		if agent.active and agent.condition(context):
			triggered.append(agent.action(context))

	return triggered


@dataclass(slots=True)
class AgentService:
	"""In-memory agent service used for chat-triggered automation."""

	agents: list[Agent] = field(default_factory=build_default_agents)

	def evaluate_agents(self, context: Context) -> list[str]:
		"""Run all agents against the provided context."""

		return evaluate_agents(context, self.agents)
