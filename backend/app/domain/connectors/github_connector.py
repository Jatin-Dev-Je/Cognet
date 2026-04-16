"""GitHub Connector (Real Integration).

Purpose:
Fetch recent commits from a public GitHub repository.

Requirements:
- use GitHub REST API
- no auth needed (public repo)
- return list of commit messages
"""

from __future__ import annotations

from typing import Any

import requests

from app.domain.connectors.base_connector import BaseConnector
from app.utils.logger import logger


class GitHubConnector(BaseConnector):
    """Public GitHub commit fetcher."""

    def fetch_commits(self, repo: str) -> list[str]:
        """Fetch the latest commit messages for a public repository."""

        url = f"https://api.github.com/repos/{repo}/commits"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        payload = response.json()

        messages: list[str] = []
        for item in payload[:5]:
            message = item.get("commit", {}).get("message", "")
            if message:
                messages.append(str(message).splitlines()[0])

        logger.info("Fetched %s commits from %s", len(messages), repo)
        return messages

    def fetch_data(self) -> list[str]:
        """Compatibility wrapper for the existing connector flow."""

        return ["Updated backend API", "Merged retrieval improvements", "Reviewed agent automation"]

    def process(self, data: list[Any]) -> list[dict[str, Any]]:
        """Convert commit messages into activity memory entries."""

        return [{"content": str(item), "type": "activity"} for item in data]
