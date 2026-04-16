"""Health Check Endpoint.

Purpose:
Verify backend is running.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.core.response.contracts import success_response


router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, object]:
	return success_response({"status": "ok"}, meta={"endpoint": "health"})