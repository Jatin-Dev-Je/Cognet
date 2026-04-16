"""Central Core Configuration.

Purpose:
Expose high-value configuration values to core system modules without hardcoding secrets.
"""

from __future__ import annotations

from dataclasses import dataclass
import os

from app.config.settings import get_settings


@dataclass(slots=True)
class CoreConfig:
	mongo_url: str
	openai_key: str | None
	jwt_secret: str
	jwt_algorithm: str
	jwt_expiry_hours: int
	cache_enabled: bool
	redis_url: str | None


def get_core_config() -> CoreConfig:
	settings = get_settings()
	return CoreConfig(
		mongo_url=settings.mongodb_uri,
		openai_key=os.getenv("OPENAI_KEY", os.getenv("COGNET_OPENAI_KEY")),
		jwt_secret=settings.jwt_secret,
		jwt_algorithm=settings.jwt_algorithm,
		jwt_expiry_hours=settings.jwt_expiry_hours,
		cache_enabled=settings.cache_enabled,
		redis_url=settings.redis_url,
	)


MONGO_URL = get_core_config().mongo_url
OPENAI_KEY = get_core_config().openai_key