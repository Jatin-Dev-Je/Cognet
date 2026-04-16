"""Request Context.

Purpose:
Carry metadata across entire request lifecycle.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter


@dataclass(slots=True)
class RequestContext:
	user_id: str | None
	request_id: str
	start_time: float | None = field(default=None)

	def start(self) -> None:
		self.start_time = perf_counter()

	def elapsed_ms(self) -> int:
		if self.start_time is None:
			return 0
		return int((perf_counter() - self.start_time) * 1000)