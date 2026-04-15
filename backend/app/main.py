"""App entry point."""

from __future__ import annotations

from fastapi import FastAPI

from app.api.router import api_router
from app.core.events.event_bus import event_bus
from app.utils.logger import logger


app = FastAPI(title="Cognet")
app.include_router(api_router)


@app.on_event("startup")
def startup_event() -> None:
	"""Register default internal event handlers."""

	event_bus.subscribe("memory_created", lambda data: logger.info("memory_created: %s", data.get("content", "")))
	event_bus.subscribe("webhook_received", lambda data: logger.info("webhook_received: %s", data))
	event_bus.subscribe("connector_synced", lambda data: logger.info("connector_synced: %s", data))


@app.get("/")
def health() -> dict[str, str]:
	"""Basic health endpoint."""

	return {"status": "ok", "service": "cognet"}
