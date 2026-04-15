"""Context schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ContextQuery(BaseModel):
	"""Validated query for context lookup."""

	user_id: str = Field(default="developer", min_length=1, max_length=128)
	session_id: str | None = Field(default=None, max_length=128)
