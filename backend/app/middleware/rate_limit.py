"""Rate limiting middleware for Cognet."""

from __future__ import annotations

from collections import defaultdict, deque
from time import time

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


_REQUESTS: dict[str, deque[float]] = defaultdict(deque)


def is_allowed(user_id: str, *, limit: int = 20, window_seconds: int = 60) -> bool:
	now = time()
	window = _REQUESTS[user_id]
	while window and now - window[0] > window_seconds:
		window.popleft()
	if len(window) >= limit:
		return False
	window.append(now)
	return True


class RateLimitMiddleware(BaseHTTPMiddleware):
	"""Simple in-memory per-user rate limiting."""

	async def dispatch(self, request: Request, call_next) -> Response:
		if request.url.path in {"/", "/healthz", "/readyz"} or request.url.path.startswith("/api/v1/health"):
			return await call_next(request)

		request_context = getattr(request.state, "request_context", None)
		user_id = getattr(request_context, "user_id", None) or getattr(request.state, "user_id", None) or (request.client.host if request.client else "anonymous")
		if not is_allowed(str(user_id)):
			return JSONResponse(
				status_code=status.HTTP_429_TOO_MANY_REQUESTS,
				content={"success": False, "data": {}, "meta": {}, "error": "Rate limit exceeded"},
			)

		return await call_next(request)