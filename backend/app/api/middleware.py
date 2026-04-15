"""API middleware for Cognet."""

from __future__ import annotations

from time import perf_counter
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import logger


class RequestContextMiddleware(BaseHTTPMiddleware):
	"""Attach request metadata and timing headers to every response."""

	async def dispatch(self, request: Request, call_next) -> Response:
		request_id = request.headers.get("X-Request-ID") or str(uuid4())
		request.state.request_id = request_id
		started_at = perf_counter()

		try:
			response = await call_next(request)
		except Exception as exc:
			logger.error("Unhandled request error [%s]: %s", request_id, exc)
			raise

		elapsed_ms = int((perf_counter() - started_at) * 1000)
		response.headers["X-Request-ID"] = request_id
		response.headers["X-Process-Time-ms"] = str(elapsed_ms)
		return response
