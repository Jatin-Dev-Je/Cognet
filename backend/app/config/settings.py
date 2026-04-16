"""Configuration settings for Cognet.

Memory Persistence Rules:
- load local env values when present
- prefer environment variables over the `.env` file
- keep MongoDB, API, and logging values centralized
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
import os
from pathlib import Path


def _parse_bool(value: str | None, default: bool = False) -> bool:
	if value is None:
		return default
	return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_csv(value: str | None, default: list[str] | None = None) -> list[str]:
	if not value:
		return list(default or [])
	return [item.strip() for item in value.split(",") if item.strip()]


def _load_env_file() -> None:
	"""Load backend/.env if it exists without overriding real env vars."""

	env_path = Path(__file__).resolve().parents[2] / ".env"
	if not env_path.exists():
		return

	for raw_line in env_path.read_text(encoding="utf-8").splitlines():
		line = raw_line.strip()
		if not line or line.startswith("#") or "=" not in line:
			continue
		key, value = line.split("=", 1)
		os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@dataclass(slots=True)
class Settings:
	"""Runtime settings loaded from environment variables."""

	environment: str = field(default_factory=lambda: os.getenv("ENVIRONMENT", os.getenv("COGNET_ENV", "development")))
	app_name: str = field(default_factory=lambda: os.getenv("APP_NAME", os.getenv("COGNET_APP_NAME", "Cognet")))
	api_prefix: str = field(default_factory=lambda: os.getenv("API_V1_PREFIX", os.getenv("COGNET_API_PREFIX", "/api/v1")))
	mongodb_uri: str = field(default_factory=lambda: os.getenv("MONGODB_URI", "mongodb://localhost:27017/cognet"))
	jwt_secret: str = field(default_factory=lambda: os.getenv("JWT_SECRET", os.getenv("COGNET_JWT_SECRET", "dev-only-secret-change-me-now-123456")))
	jwt_algorithm: str = field(default_factory=lambda: os.getenv("JWT_ALGORITHM", os.getenv("COGNET_JWT_ALGORITHM", "HS256")))
	jwt_expiry_hours: int = field(default_factory=lambda: int(os.getenv("JWT_EXPIRY_HOURS", os.getenv("COGNET_JWT_EXPIRY_HOURS", "24"))))
	redis_url: str | None = field(default_factory=lambda: os.getenv("REDIS_URL", os.getenv("COGNET_REDIS_URL")))
	cache_enabled: bool = field(default_factory=lambda: _parse_bool(os.getenv("COGNET_CACHE_ENABLED"), default=True))
	debug: bool = field(default_factory=lambda: _parse_bool(os.getenv("COGNET_DEBUG"), default=os.getenv("ENVIRONMENT", "development") != "production"))
	log_level: str = field(default_factory=lambda: os.getenv("COGNET_LOG_LEVEL", os.getenv("LOG_LEVEL", "INFO")))
	cors_origins: list[str] = field(default_factory=lambda: _parse_csv(os.getenv("COGNET_CORS_ORIGINS"), default=["http://localhost:3000"]))
	max_context_memories: int = field(default_factory=lambda: int(os.getenv("COGNET_MAX_CONTEXT_MEMORIES", "30")))
	retrieval_top_k: int = field(default_factory=lambda: int(os.getenv("COGNET_RETRIEVAL_TOP_K", "5")))
	request_timeout_seconds: int = field(default_factory=lambda: int(os.getenv("COGNET_REQUEST_TIMEOUT_SECONDS", "30")))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
	"""Return cached runtime settings."""

	_load_env_file()
	return Settings()
