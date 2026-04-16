"""Startup / shutdown lifecycle for Cognet."""

from __future__ import annotations

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.core.events.event_bus import event_bus
from app.infrastructure.db.mongo.collections import ensure_indexes
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
	"""Register internal event handlers and manage app lifecycle."""

	logger.info("Mongo index plan: %s", ensure_indexes())
	event_bus.subscribe("memory_created", lambda data: logger.info("memory_created: %s", data.get("content", "")))
	event_bus.subscribe("webhook_received", lambda data: logger.info("webhook_received: %s", data))
	event_bus.subscribe("connector_synced", lambda data: logger.info("connector_synced: %s", data))
	logger.info("Cognet startup complete")
	try:
		yield
	finally:
		logger.info("Cognet shutdown complete")
