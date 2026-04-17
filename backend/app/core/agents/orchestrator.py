"""Multi-agent orchestrator for Cognet."""

from __future__ import annotations

from typing import Any, Mapping

from app.core.agents.evolution import evolve_agents
from app.core.agents.memory import store_agent_memory
from app.core.agents.performance import update_score
from app.core.agents.critic import CriticAgent
from app.core.agents.planner import PlannerAgent
from app.core.agents.selector import select_executor
from app.core.context.final_formatter import format_final


def run_agents(fused_context: Mapping[str, Any]) -> str:
	planner = PlannerAgent()
	critic = CriticAgent()

	plan = planner.run(fused_context)
	executor = select_executor(fused_context)
	result = executor.run(fused_context)
	final_step = critic.run(result)

	prediction = dict(fused_context.get("prediction") or {})

	reasoning = str(fused_context.get("reasoning") or "").strip()
	insight = str(fused_context.get("insight") or "").strip()
	completed = list(fused_context.get("completed", []))

	store_agent_memory("planner", fused_context, plan)
	store_agent_memory("executor", fused_context, result)
	store_agent_memory("critic", result, final_step)
	update_score("planner", 0.8)
	update_score("executor", 0.9 if final_step.startswith("Focus on") else 0.4)
	update_score("critic", 0.9 if final_step != result else 0.5)

	formatted = format_final(
		fused_context,
		final_step,
		prediction=prediction.get("prediction") if prediction.get("prediction") else None,
		reasoning=reasoning,
		insight=insight or "You're progressing through backend development stages.",
		completed=completed,
	)

	return formatted.strip()