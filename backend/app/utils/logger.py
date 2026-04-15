"""Logger setup for Cognet.

Purpose:
Provide a shared logger for requests, errors, and key events.
"""

from __future__ import annotations

import logging


logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("cognet")
logger.propagate = False