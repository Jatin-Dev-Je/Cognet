"""Logger setup for Cognet.

Purpose:
Provide a shared logger for requests, errors, and key events.
"""

from __future__ import annotations

import logging


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("cognet")