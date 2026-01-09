from __future__ import annotations

from fastapi import APIRouter

from backend.app.api.v1.endpoints import health, youtube

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(youtube.router, prefix="/youtube", tags=["youtube"])
