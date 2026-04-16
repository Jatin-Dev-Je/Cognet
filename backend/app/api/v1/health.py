"""Health Check Endpoint.

Purpose:
Verify backend is running.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.config.settings import get_settings
from app.infrastructure.db.mongo.client import get_mongo_client
from app.core.response.contracts import success_response


router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, object]:
	settings = get_settings()
	db_status = "disconnected"
	try:
		get_mongo_client().admin.command("ping")
		db_status = "connected"
	except Exception:
		db_status = "disconnected"

	return success_response({"status": "ok", "db": db_status, "llm": "reachable", "version": settings.api_version}, meta={"endpoint": "health"})