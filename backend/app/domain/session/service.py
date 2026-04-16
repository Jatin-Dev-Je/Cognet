"""Session Service for Cognet.

Purpose:
Track current working context for a user session.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.core.identity import generate_id


SessionRecord = dict[str, Any]


@dataclass(slots=True)
class SessionService:
	"""In-memory session continuity store."""

	storage: dict[str, SessionRecord] = field(default_factory=dict)

	def get_current_session(self, user_id: str, session_id: str | None = None) -> SessionRecord:
		"""Return the active session context for a user."""

		key = session_id or user_id
		session = self.storage.get(key)
		if session is None:
			session = {
				"id": generate_id(),
				"session_id": key,
				"user_id": user_id,
				"active_project": None,
				"recent_actions": [],
				"version": 1,
				"is_deleted": False,
			}
			self.storage[key] = session
		return session

	def update_session(self, user_id: str, session_id: str | None, active_project: str | None, recent_action: str | None) -> SessionRecord:
		"""Update the current session with latest activity."""

		session = self.get_current_session(user_id, session_id=session_id)
		if active_project:
			session["active_project"] = active_project
		if recent_action:
			session["recent_actions"].append(recent_action)
			session["recent_actions"] = session["recent_actions"][-5:]
		session["version"] = int(session.get("version", 1)) + 1
		return session

	def soft_delete_session(self, session_id: str) -> SessionRecord | None:
		session = self.storage.get(session_id)
		if session is None:
			return None
		session["is_deleted"] = True
		session["version"] = int(session.get("version", 1)) + 1
		return session