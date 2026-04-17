"""Base Agent for Cognet multi-agent flows."""

from __future__ import annotations

from typing import Any, Mapping


class BaseAgent:
	def run(self, context: Mapping[str, Any]):
		raise NotImplementedError