"""Endpoints for generating tweets."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/{tweet_id}")
def like(tweet_id: int):
    """Like a tweet by id."""
    print(tweet_id)
