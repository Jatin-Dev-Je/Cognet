from __future__ import annotations

from datetime import datetime, timedelta

from app.core.ai.prompt import build_chat_prompt
from app.core.context.temporal_builder import group_by_time
from app.core.context.formatter import format_temporal_context
from app.core.retrieval.scoring import temporal_score
from app.domain.memory.entity import get_day_bucket


def test_day_bucket_classifies_recent_dates() -> None:
	assert get_day_bucket(datetime.utcnow()) == "today"
	assert get_day_bucket(datetime.utcnow() - timedelta(days=1)) == "yesterday"
	assert get_day_bucket(datetime.utcnow() - timedelta(days=3)) == "this_week"
	assert get_day_bucket(datetime.utcnow() - timedelta(days=30)) == "older"


def test_group_by_time_builds_temporal_context() -> None:
	memory_docs = [
		{"content": "Today work", "day_bucket": "today"},
		{"content": "Yesterday work", "day_bucket": "yesterday"},
		{"content": "Week work", "day_bucket": "this_week"},
	]

	grouped = group_by_time(memory_docs)
	formatted = format_temporal_context(grouped)

	assert grouped["today"] == ["Today work"]
	assert "Today:" in formatted
	assert "Yesterday:" in formatted
	assert "This Week:" in formatted


def test_temporal_score_prioritizes_recent_memory() -> None:
	assert temporal_score({"day_bucket": "today"}) > temporal_score({"day_bucket": "this_week"})
	assert temporal_score({"day_bucket": "yesterday"}) > temporal_score({"day_bucket": "older"})


def test_prompt_includes_temporal_sections() -> None:
	prompt = build_chat_prompt(
		"What should I do next?",
		"Context block",
		["Suggested next step: refine retrieval"],
		temporal_context="Today:\n- improve retrieval",
		next_step="Focus on: test edge cases",
	)

	assert "Temporal Context:" in prompt
	assert "Next Step:" in prompt