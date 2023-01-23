"""Endpoints for generating tweets."""
from fastapi import APIRouter, Depends

from app.api import deps, schemas
from app.api.endpoints.generate import generate_post


router = APIRouter()
@router.get("", response_model=schemas.Tweet)
def regenerate(current_user: str = Depends(deps.get_current_user)):
    """Regenerate a tweet for the user."""
    print(current_user)
    return generate_post(current_user, rerun_whole=True)
