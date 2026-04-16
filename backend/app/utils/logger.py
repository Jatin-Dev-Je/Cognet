"""Logger Setup.

Purpose:
Track system behavior.

Should log:
- user input
- memory stored
- retrieval count
- response time
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
import logging
import os
from typing import Any


class JsonFormatter(logging.Formatter):
	"""Format logs as JSON for production observability."""

	def format(self, record: logging.LogRecord) -> str:
		payload = {
			"timestamp": datetime.now(timezone.utc).isoformat(),
			"level": record.levelname,
			"logger": record.name,
			"event": getattr(record, "event", record.getMessage()),
			"message": record.getMessage(),
		}
		if hasattr(record, "user_id"):
			payload["user_id"] = getattr(record, "user_id")
		if hasattr(record, "data"):
			payload["data"] = getattr(record, "data")
		if hasattr(record, "request_id"):
			payload["request_id"] = getattr(record, "request_id")
		return json.dumps(payload, default=str)


def _resolve_level() -> int:
	level_name = os.getenv("COGNET_LOG_LEVEL", os.getenv("LOG_LEVEL", "INFO")).upper()
	return getattr(logging, level_name, logging.INFO)


logger = logging.getLogger("cognet")
logger.setLevel(_resolve_level())
logger.propagate = False

if not logger.handlers:
	handler = logging.StreamHandler()
	handler.setFormatter(JsonFormatter())
	logger.addHandler(handler)


def log_event(event: str, data: dict[str, Any] | None = None, *, user_id: str | None = None, level: int = logging.INFO) -> None:
	"""Log a structured event."""

	logger.log(level, event, extra={"event": event, "data": data or {}, "user_id": user_id})