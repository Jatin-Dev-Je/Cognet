"""Logging middleware for Cognet."""

from __future__ import annotations

from time import perf_counter
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.context.request_context import RequestContext
from app.utils.logger import log_event


class LoggingMiddleware(BaseHTTPMiddleware):
	"""Attach request metadata, timing, and structured logs to responses."""

	async def dispatch(self, request: Request, call_next) -> Response:
		request_id = request.headers.get("X-Request-ID") or str(uuid4())
		request.state.request_id = request_id
		request_context = getattr(request.state, "request_context", None)
		if request_context is None:
			request_context = RequestContext(user_id=getattr(request.state, "user_id", None), request_id=request_id)
			request.state.request_context = request_context
		request_context.start()
		started_at = perf_counter()
		response = await call_next(request)
		elapsed_ms = int((perf_counter() - started_at) * 1000)
		response.headers["X-Request-ID"] = request_id
		response.headers["X-Process-Time-ms"] = str(elapsed_ms)
		log_event(
			"request_completed",
			{
				"method": request.method,
				"path": str(request.url.path),
				"status_code": response.status_code,
				"elapsed_ms": elapsed_ms,
			},
			user_id=request_context.user_id,
			request_id=request_id,
		)
		return response