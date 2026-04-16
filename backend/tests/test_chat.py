"""Test Chat Endpoint.

Purpose:
Ensure /chat returns a valid response.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.core.auth.jwt import create_token
from app.main import app


def test_chat_endpoint_returns_response() -> None:
	client = TestClient(app)
	token = create_token("test-user")
	response = client.post(
		"/api/v1/chat",
		json={"message": "I am building Cognet backend"},
		headers={"Authorization": f"Bearer {token}"},
	)

	assert response.status_code == 200
	body = response.json()
	assert body["success"] is True
	assert "response" in body["data"]