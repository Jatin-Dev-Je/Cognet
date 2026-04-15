"""App entry point."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.api.middleware import RequestContextMiddleware
from app.config.settings import get_settings
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
app.add_middleware(RequestContextMiddleware)
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
	return JSONResponse(status_code=422, content={"detail": exc.errors(), "status": "validation_error"})


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
	return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
	logger.exception("Unhandled server error: %s", exc)
	return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/")
def health() -> dict[str, str]:
	"""Basic health endpoint."""

	return {"status": "ok", "service": settings.app_name.lower()}


@app.get("/healthz")
def healthz() -> dict[str, str]:
	"""Liveness probe."""

	return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict[str, str]:
	"""Readiness probe."""

	return {"status": "ready"}
