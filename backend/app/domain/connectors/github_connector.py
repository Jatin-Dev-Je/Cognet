"""GitHub mock connector for Cognet.

Purpose:
Simulate external GitHub activity ingestion.
"""

from __future__ import annotations

from typing import Any

from app.domain.connectors.base_connector import BaseConnector


class GitHubConnector(BaseConnector):
    """Mock GitHub connector for local development."""

    def fetch_data(self) -> list[str]:
        """Fetch mock GitHub activity."""

        return ["Updated backend API", "Merged retrieval improvements", "Reviewed agent automation"]

    def process(self, data: list[Any]) -> list[dict[str, Any]]:
        """Convert GitHub activity into memory-like records."""

        return [{"content": str(item), "type": "activity"} for item in data]
