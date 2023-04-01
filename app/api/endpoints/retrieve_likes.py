"""Endpoint for retrieving tweets liked by a user."""

from fastapi import APIRouter, Depends

from app.api import deps
from app.api.db import get_user_liked_tweets

router = APIRouter()


@router.get("")
def retrieve_liked_tweets(current_user: str = Depends(deps.get_current_user_id)):
    """Retrieve a tweet by id."""
    return get_user_liked_tweets(current_user)
