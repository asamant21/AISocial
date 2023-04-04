"""Endpoint for retrieving tweets liked by a user."""

from fastapi import APIRouter, Depends

from app.api import deps
from app.api.db import post_new_style

router = APIRouter()

@router.post("/{style}")
async def change_style(style: str, current_user: str = Depends(deps.get_current_user_id)):
    """Change preferred tweet style for the given user."""
    return post_new_style(style, current_user)
