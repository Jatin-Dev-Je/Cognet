"""Retry and timeout helpers for Cognet."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar


T = TypeVar("T")


async def retry(func: Callable[[], Awaitable[T]], retries: int = 3) -> T:
	last_error: Exception | None = None
	for _ in range(retries):
		try:
			return await func()
		except Exception as exc:
			last_error = exc
			await asyncio.sleep(1)
	if last_error is None:
		raise Exception("Failed after retries")
	raise last_error


async def with_timeout(coro: Awaitable[T], timeout: int = 5) -> T:
	return await asyncio.wait_for(coro, timeout=timeout)