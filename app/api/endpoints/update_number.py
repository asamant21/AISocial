"""Endpoints for generating tweets."""
from fastapi import APIRouter, Depends

from app.api import deps

router = APIRouter()


@router.get("/{phone_number}")
def update_number(
    phone_number: str,
    user_jwt: str = Depends(deps.get_current_user_jwt),
):
    """Regenerate a tweet for the user."""
    print(user_jwt)
    deps.update_user_phone_number(user_jwt, phone_number)



