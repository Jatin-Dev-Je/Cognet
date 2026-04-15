"""Configuration settings for Cognet."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
import os


def _parse_bool(value: str | None, default: bool = False) -> bool:
	if value is None:
		return default
	return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_csv(value: str | None, default: list[str] | None = None) -> list[str]:
	if not value:
		return list(default or [])
	return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(slots=True)
class Settings:
	"""Runtime settings loaded from environment variables."""

	environment: str = field(default_factory=lambda: os.getenv("COGNET_ENV", "development"))
	app_name: str = field(default_factory=lambda: os.getenv("COGNET_APP_NAME", "Cognet"))
	api_prefix: str = field(default_factory=lambda: os.getenv("COGNET_API_PREFIX", "/api/v1"))
	debug: bool = field(default_factory=lambda: _parse_bool(os.getenv("COGNET_DEBUG"), default=True))
	log_level: str = field(default_factory=lambda: os.getenv("COGNET_LOG_LEVEL", "INFO"))
	cors_origins: list[str] = field(default_factory=lambda: _parse_csv(os.getenv("COGNET_CORS_ORIGINS"), default=["http://localhost:3000"]))
	max_context_memories: int = field(default_factory=lambda: int(os.getenv("COGNET_MAX_CONTEXT_MEMORIES", "30")))
	retrieval_top_k: int = field(default_factory=lambda: int(os.getenv("COGNET_RETRIEVAL_TOP_K", "5")))
	request_timeout_seconds: int = field(default_factory=lambda: int(os.getenv("COGNET_REQUEST_TIMEOUT_SECONDS", "30")))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
	"""Return cached runtime settings."""

	return Settings()
