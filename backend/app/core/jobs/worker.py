"""Background Job Worker for Cognet."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable


def run_background(task: Awaitable[object]) -> asyncio.Task[object]:
	"""Schedule an async task outside the main request flow."""

	return asyncio.create_task(task)