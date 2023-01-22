"""Initialize routers."""

from fastapi import APIRouter
from app.api.endpoints import generate, like

api_router = APIRouter()
api_router.include_router(generate.router, prefix="/generate", tags=["generate"])
api_router.include_router(like.router, prefix="/like", tags=["like"])
