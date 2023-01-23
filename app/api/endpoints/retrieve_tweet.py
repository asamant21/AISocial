"""Endpoint for retrieving tweets."""

from fastapi import APIRouter, Depends

from app.api import deps, schemas
from app.api.db import get_user_tweet_view

router = APIRouter()


@router.get("/{tweet_id}", response_model=schemas.UserTweetView)
def retrieve_tweet(tweet_id: int, current_user: str = Depends(deps.get_current_user)):
    """Retrieve a tweet by id."""
    return get_user_tweet_view(tweet_id, current_user)
