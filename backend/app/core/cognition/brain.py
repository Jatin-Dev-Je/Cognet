"""Cognitive brain for Cognet."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from app.core.cognition.action import act
from app.core.cognition.learning import learn
from app.core.cognition.memory import get_memory_state
from app.core.cognition.perception import perceive_input
from app.core.cognition.planning import plan
from app.core.cognition.reasoning import reason
from app.core.context.final_formatter import format_final
from app.core.prediction.proactive import run_prediction


def run_cognition(
	user_id: str,
	message: str,
	memories: Sequence[dict[str, Any]] | None = None,
	context: Mapping[str, Any] | None = None,
	prediction: Mapping[str, Any] | None = None,
	temporal: Mapping[str, list[str]] | None = None,
) -> dict[str, Any]:
	perception = perceive_input(message)
	memory_list, memory_temporal = get_memory_state(memories or [])
	reasoning_state = reason(memory_list)
	prediction_state = dict(prediction or run_prediction(memory_list))
	structured_context = dict(context or {})
	plan_step = plan(structured_context, prediction_state)
	action = act(plan_step, structured_context)
	learning_state = learn(user_id, action)
	combined_temporal = dict(temporal or memory_temporal)
	fused_context = {
		"temporal": combined_temporal,
		"completed": list(structured_context.get("completed", [])),
		"recent": [memory.get("content", "") for memory in memory_list],
	}
	response = format_final(
		fused_context,
		plan_step,
		prediction=prediction_state.get("prediction") if prediction_state.get("prediction") else None,
		reasoning=reasoning_state["reasoning"],
		insight=reasoning_state["insight"],
		completed=list(structured_context.get("completed", [])),
	)

	return {
		"perception": perception,
		"memory_state": memory_list,
		"temporal": combined_temporal,
		"reasoning": reasoning_state["reasoning"],
		"insight": reasoning_state["insight"],
		"chain": reasoning_state["chain"],
		"ordered_chain": reasoning_state["ordered"],
		"reasoning_context": reasoning_state["expanded_context"],
		"reasoning_graph": reasoning_state["graph"],
		"prediction": prediction_state,
		"plan": plan_step,
		"action": action,
		"learning": learning_state,
		"response": response,
	}