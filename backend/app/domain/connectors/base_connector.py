"""Base Connector Interface for Cognet.

Purpose:
Define a small contract for external tool connectors.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseConnector(ABC):
    """Base class for all connectors."""

    @abstractmethod
    def fetch_data(self) -> list[Any]:
        """Fetch raw data from an external source."""

    @abstractmethod
    def process(self, data: list[Any]) -> list[dict[str, Any]]:
        """Process raw connector data into Cognet memory records."""
