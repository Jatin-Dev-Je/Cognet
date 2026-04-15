"""Memory schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class MemoryCreateRequest(BaseModel):
	"""Validated memory creation payload."""

	user_id: str = Field(default="developer", min_length=1, max_length=128)
	content: str = Field(min_length=1, max_length=8000)
	session_id: str | None = Field(default=None, max_length=128)
	goal: str | None = Field(default=None, max_length=8000)
