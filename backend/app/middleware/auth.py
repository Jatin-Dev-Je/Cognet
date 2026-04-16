"""Authentication middleware for Cognet."""

from __future__ import annotations

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.context.request_context import RequestContext
from app.core.auth.jwt import verify_token


class AuthMiddleware(BaseHTTPMiddleware):
	"""Validate bearer tokens and attach user_id to the request state."""

	async def dispatch(self, request: Request, call_next) -> Response:
		if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi"):
			return await call_next(request)

		if request.url.path in {"/", "/healthz", "/readyz"} or request.url.path.startswith("/api/v1/health"):
			return await call_next(request)

		authorization = request.headers.get("Authorization")
		if not authorization or not authorization.startswith("Bearer "):
			return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"success": False, "data": {}, "meta": {}, "error": "Missing bearer token"})

		token = authorization.split(" ", 1)[1].strip()
		try:
			payload = verify_token(token)
		except Exception:
			return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"success": False, "data": {}, "meta": {}, "error": "Invalid authentication token"})

		request.state.user_id = str(payload["user_id"])
		request_context = getattr(request.state, "request_context", None)
		if request_context is None:
			request_context = RequestContext(user_id=str(payload["user_id"]), request_id=str(request.headers.get("X-Request-ID") or "unknown"))
		else:
			request_context.user_id = str(payload["user_id"])
		request.state.request_context = request_context
		return await call_next(request)