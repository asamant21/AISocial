"""Endpoints for generating tweets."""
from datetime import datetime

from fastapi import APIRouter, Depends

from app.api import deps, schemas
from app.api.endpoints.generate import generate_post

router = APIRouter()


@router.get("", response_model=schemas.Tweet)
def regenerate(
    current_user: str = Depends(deps.get_current_user),
    regen_time: datetime = Depends(deps.update_regen_time),
):
    """Regenerate a tweet for the user."""
    print(current_user)
    return generate_post(current_user, regen_time)


