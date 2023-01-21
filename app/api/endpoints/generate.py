"""Endpoints for generating tweets."""
from typing import List

from fastapi import APIRouter

from api import schemas
from config import supabase

router = APIRouter()


@router.get("", response_model=schemas.Tweet)
def generate():
    """Generate a tweet for the user."""

    return {"id": 1, "content": "foo", "author": "foo"}


def generate_post(user_id: int) -> dict:
    # Impression data schema:
    # [{'id': 1,
    #   'created_at': '2023-01-21T22:09:53+00:00',
    #   'tweet_id': 1,
    #   'user_id': 1,
    #   'child_like_count': 1,
    #   'liked': True}]
    impressions = (
        supabase.table("Impression").select("*").filter("user_id", "eq", user_id).execute().data
    )
    weights = compute_weights(impressions)
    examples = choose_examples(weights)
    tweet = generate_tweet_from_examples(examples)
    # Tweet data schema:
    # [{'id': 6,
    #   'created_at': '2023-01-21T22:54:52.770345+00:00',
    #   'content': 'insert',
    #   'author': 'test2',
    #   'metadata': {}}]
    insert_resp = supabase.table("Tweet").insert(tweet).execute().data[0]
    return {
        "id": insert_resp["id"],
        "author": insert_resp["author"],
        "content": insert_resp["content"]
    }


def compute_weights(impressions: List[dict]) -> dict:
    return {i["id"]: i["child_like_count"] for i in impressions}


def choose_examples(weights: dict) -> List[str]:
    return ["x_user: example 1", "y_user: example 2"]


def generate_tweet_from_examples(examples: List[str]) -> dict:
    return {"content": "foo", "author": "foo"}
