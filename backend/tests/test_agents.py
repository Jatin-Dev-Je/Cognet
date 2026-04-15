from app.core.inference.agent_runner import run_agents
from app.domain.agent.service import AgentService, focus_agent_action, focus_agent_condition, task_reminder_action, task_reminder_condition


def test_agent_service_triggers_task_reminder() -> None:
	context = {"tasks": ["Improve retrieval"]}
	agent_service = AgentService()

	results = agent_service.evaluate_agents(context)

	assert any("pending tasks" in result for result in results)


def test_agent_runner_triggers_focus_suggestion() -> None:
	agents = AgentService().agents
	context = {"tasks": ["Improve retrieval", "Add tests", "Refine prompts"]}

	results = run_agents(context, agents)

	assert any("Focus on one" in result for result in results)