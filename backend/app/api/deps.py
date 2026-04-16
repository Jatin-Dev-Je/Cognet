"""Authentication Dependency.

Purpose:
Extract user_id from request.

For now:
- return fixed demo user

Later:
- replace with JWT decoding
"""

from __future__ import annotations


def get_current_user() -> str:
	"""Return the demo user until real auth is wired up."""

	return "demo_user"
