"""API router."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import chat, connectors, context, insights, memory, webhooks


api_router = APIRouter()
api_router.include_router(chat.router)
api_router.include_router(memory.router)
api_router.include_router(context.router)
api_router.include_router(insights.router)
api_router.include_router(connectors.router)
api_router.include_router(webhooks.router)
