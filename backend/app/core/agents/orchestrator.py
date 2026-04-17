"""Multi-agent orchestrator for Cognet."""

from __future__ import annotations

from typing import Any, Mapping

from app.core.agents.evolution import evolve_agents
from app.core.agents.memory import store_agent_memory
from app.core.agents.performance import update_score
from app.core.agents.critic import CriticAgent
from app.core.agents.planner import PlannerAgent
from app.core.agents.selector import select_executor


def _format_temporal_sections(fused_context: Mapping[str, Any]) -> str:
	text = ""
	temporal = dict(fused_context.get("temporal", {}))

	if temporal.get("today"):
		text += "Today:\n"
		for item in temporal["today"]:
			text += f"- {item}\n"

	if temporal.get("yesterday"):
		text += "\nYesterday:\n"
		for item in temporal["yesterday"]:
			text += f"- {item}\n"

	if temporal.get("this_week"):
		text += "\nThis Week:\n"
		for item in temporal["this_week"]:
			text += f"- {item}\n"

	if not text:
		for item in list(fused_context.get("recent", [])):
			text += f"- {item}\n"

	return text.strip()


def run_agents(fused_context: Mapping[str, Any]) -> str:
	planner = PlannerAgent()
	critic = CriticAgent()

	plan = planner.run(fused_context)
	executor = select_executor(fused_context)
	result = executor.run(fused_context)
	final_step = critic.run(result)
	state = evolve_agents()

	prediction = dict(fused_context.get("prediction") or {})
	prediction_line = ""
	if prediction.get("prediction"):
		prediction_line = f"\nPrediction:\n{prediction['prediction']}\n"

	sections = _format_temporal_sections(fused_context)
	completed = list(fused_context.get("completed", []))
	completed_text = "\n".join(f"- {item}" for item in completed) or "- None"

	store_agent_memory("planner", fused_context, plan)
	store_agent_memory("executor", fused_context, result)
	store_agent_memory("critic", result, final_step)
	update_score("planner", 0.8)
	update_score("executor", 0.9 if final_step.startswith("Focus on") else 0.4)
	update_score("critic", 0.9 if final_step != result else 0.5)

	return f"""
{sections}

Completed:
{completed_text}

Next Step:
{final_step}

{prediction_line}Insight:
You're progressing through backend development stages.

Agent State:
{state}
""".strip()