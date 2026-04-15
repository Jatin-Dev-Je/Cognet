"""Event Bus for Cognet.

Purpose:
Handle internal system events.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable


EventHandler = Callable[[Any], None]


class EventBus:
    """Simple in-memory event bus."""

    def __init__(self) -> None:
        self.listeners: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, event: str, handler: EventHandler) -> None:
        """Register an event handler."""

        self.listeners[event].append(handler)

    def publish(self, event: str, data: Any) -> None:
        """Publish an event to all registered handlers."""

        for handler in self.listeners.get(event, []):
            handler(data)


event_bus = EventBus()
