"""Authentication Dependency.

Purpose:
Extract user_id from the authenticated request.
"""

from __future__ import annotations

from fastapi import Header, HTTPException, Request, status

from app.core.context.request_context import RequestContext
from app.core.auth.jwt import verify_token


def get_current_user(request: Request, authorization: str | None = Header(default=None, alias="Authorization")) -> str:
	"""Return the authenticated user_id from request state or bearer token."""

	user_id = getattr(request.state, "user_id", None)
	if user_id:
		request_context = getattr(request.state, "request_context", None)
		if request_context is None:
			request_context = RequestContext(user_id=str(user_id), request_id=str(request.headers.get("X-Request-ID") or "unknown"))
		else:
			request_context.user_id = str(user_id)
		request.state.request_context = request_context
		return str(user_id)

	if not authorization or not authorization.startswith("Bearer "):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

	token = authorization.split(" ", 1)[1].strip()
	try:
		payload = verify_token(token)
	except Exception as exc:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token") from exc

	user_id = str(payload["user_id"])
	request.state.user_id = user_id
	request_context = getattr(request.state, "request_context", None)
	if request_context is None:
		request_context = RequestContext(user_id=user_id, request_id=str(request.headers.get("X-Request-ID") or "unknown"))
	else:
		request_context.user_id = user_id
	request.state.request_context = request_context
	return user_id
