"""JWT Authentication Module.

Purpose:
- create token
- verify token
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import jwt

from app.config.settings import get_settings


def _get_secret() -> str:
	settings = get_settings()
	if not settings.jwt_secret:
		raise RuntimeError("JWT secret is not configured.")
	return settings.jwt_secret


def create_token(user_id: str, expires_in_hours: int | None = None) -> str:
	settings = get_settings()
	expiry_hours = expires_in_hours if expires_in_hours is not None else settings.jwt_expiry_hours
	payload = {
		"user_id": user_id,
		"iat": datetime.utcnow(),
		"exp": datetime.utcnow() + timedelta(hours=expiry_hours),
	}
	return jwt.encode(payload, _get_secret(), algorithm=settings.jwt_algorithm)


def verify_token(token: str) -> dict[str, Any]:
	settings = get_settings()
	decoded = jwt.decode(token, _get_secret(), algorithms=[settings.jwt_algorithm])
	if "user_id" not in decoded:
		raise jwt.InvalidTokenError("Missing user_id in token payload")
	return decoded