"""Chat Use Case Flow for Cognet."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.core.intelligence.engine import IntelligenceEngine
from app.domain.memory.service import MemoryService


@dataclass(slots=True)
class ChatUseCase:
	"""Thin chat facade over the intelligence engine."""

	memory_service: MemoryService
	intelligence_engine: IntelligenceEngine | None = None

	def __post_init__(self) -> None:
		if self.intelligence_engine is None:
			self.intelligence_engine = IntelligenceEngine(memory_service=self.memory_service)

	def handle_chat(
		self,
		user_id: str,
		message: str,
		session_id: str | None = None,
		top_k: int = 5,
		memory_limit: int = 30,
	) -> dict[str, Any]:
		return self.intelligence_engine.run_intelligence(
			user_id,
			message,
			session_id=session_id,
			top_k=top_k,
			memory_limit=memory_limit,
		)
