"""Memory Classifier for Cognet.

Purpose:
Classify user input into structured types for better context understanding.

Types:
- project -> what user is working on
- completed -> finished work
- task -> pending work
- general -> fallback

Input:
- raw user text

Output:
- string type
"""

from __future__ import annotations


def classify_memory(text: str) -> str:
	"""Classify a memory string into a simple Cognet type."""

	content = text.lower()

	if "completed" in content or "done" in content or "finished" in content:
		return "completed"

	if "working on" in content or "building" in content or "implementing" in content:
		return "project"

	if "need to" in content or "todo" in content or "to do" in content or "should" in content:
		return "task"

	return "general"


def compute_importance(memory_type: str) -> float:
	"""Assign an importance score to a memory type."""

	if memory_type == "project":
		return 0.9
	if memory_type == "completed":
		return 0.8
	if memory_type == "task":
		return 0.7
	return 0.5