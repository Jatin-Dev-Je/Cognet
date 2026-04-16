"""Test Chat Endpoint.

Purpose:
Ensure /chat returns a valid response.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_chat_endpoint_returns_response() -> None:
	client = TestClient(app)
	response = client.post("/api/v1/chat", json={"message": "I am building Cognet backend"})

	assert response.status_code == 200
	assert "response" in response.json()