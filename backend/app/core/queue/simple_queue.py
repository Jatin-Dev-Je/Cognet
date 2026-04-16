"""Lightweight task queue for Cognet."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


queue: list[Callable[[], Any]] = []


def add_task(task: Callable[[], Any]) -> None:
	queue.append(task)


def run_queue() -> list[Any]:
	results: list[Any] = []
	while queue:
		task = queue.pop(0)
		results.append(task())
	return results