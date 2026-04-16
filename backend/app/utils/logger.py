"""Logger Setup.

Purpose:
Track system behavior.

Should log:
- user input
- memory stored
- retrieval count
- response time
"""

from __future__ import annotations

import logging
import os


def _resolve_level() -> int:
	level_name = os.getenv("COGNET_LOG_LEVEL", os.getenv("LOG_LEVEL", "INFO")).upper()
	return getattr(logging, level_name, logging.INFO)


logger = logging.getLogger("cognet")
logging.basicConfig(level=_resolve_level(), format="%(asctime)s %(levelname)s %(name)s %(message)s")

logger.propagate = False