"""Endpoints for generating tweets."""
import os

from api import schemas
from fastapi import APIRouter
from supabase import create_client, Client

router = APIRouter()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


@router.get("", response_model=schemas.Tweet)
def generate():
    """Generate a tweet for the user."""

    return {"id": 1, "content": "foo", "author": "foo"}


def generate_post():
    user_id = get_user_id()
    # Returned data schema:
    # [{'id': 1,
    #   'created_at': '2023-01-21T22:09:53+00:00',
    #   'tweet_id': 1,
    #   'user_id': 1,
    #   'child_like_count': 1,
    #   'liked': True}]
    impressions = supabase.table("Impression").select("*").filter("user_id", "eq", user_id).execute().data
    pass


def get_user_id():
    pass
