"""Standard API error responses."""

from __future__ import annotations

from typing import Any


def error_response(message: str, *, meta: dict[str, Any] | None = None, data: Any | None = None) -> dict[str, Any]:
	return {
		"success": False,
		"data": {} if data is None else data,
		"meta": meta or {},
		"error": message,
	}