"""App entry point."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.config.settings import get_settings
from app.core.errors import error_response
from app.core.response.contracts import success_response
from app.middleware.auth import AuthMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.lifespan import lifespan
from app.utils.logger import logger


settings = get_settings()

app = FastAPI(
	title=settings.app_name,
	debug=settings.debug,
	docs_url="/docs" if settings.environment != "production" else None,
	redoc_url=None,
	openapi_url="/openapi.json" if settings.environment != "production" else None,
	lifespan=lifespan,
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.cors_origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)
app.include_router(api_router, prefix=settings.api_prefix)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
	logger.warning("Validation error: %s", exc.errors())
	return JSONResponse(status_code=422, content=error_response("Validation failed", meta={"errors": exc.errors(), "request_id": getattr(getattr(_, 'state', None), 'request_id', None)}))


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
	message = str(exc.detail) if exc.detail is not None else "HTTP error"
	return JSONResponse(status_code=exc.status_code, content=error_response(message, meta={"status_code": exc.status_code, "request_id": getattr(getattr(_, 'state', None), 'request_id', None)}))


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
	logger.exception("Unhandled server error: %s", exc)
	return JSONResponse(status_code=500, content=error_response("Internal server error", meta={"request_id": getattr(getattr(_, 'state', None), 'request_id', None)}))


@app.get("/")
def health() -> dict[str, object]:
	"""Basic health endpoint."""

	return success_response({"status": "ok", "service": settings.app_name.lower()}, meta={"route": "root_health"})


@app.get("/healthz")
def healthz() -> dict[str, object]:
	"""Liveness probe."""

	return success_response({"status": "ok"}, meta={"route": "healthz"})


@app.get("/readyz")
def readyz() -> dict[str, object]:
	"""Readiness probe."""

	return success_response({"status": "ready"}, meta={"route": "readyz"})
