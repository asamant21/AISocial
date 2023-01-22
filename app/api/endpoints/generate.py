"""Endpoints for generating tweets."""
from typing import List, Dict

from fastapi import APIRouter

from app.api import schemas
from app.config import supabase
from app.constants import METADATA_PROMPT_TWEET_IDS, IMPRESSION_TABLE_CHILD_LIKE_COUNT, \
    IMPRESSION_TABLE_NAME, IMPRESSION_TABLE_USER_ID, TWEET_TABLE_ID, \
    TWEET_TABLE_METADATA, TWEET_TABLE_AUTHOR, TWEET_TABLE_CONTENT, TWEET_TABLE_NAME

router = APIRouter()


@router.get("", response_model=schemas.Tweet)
def generate():
    """Generate a tweet for the user."""

    return {TWEET_TABLE_ID: 1, TWEET_TABLE_CONTENT: "foo", TWEET_TABLE_AUTHOR: "foo"}


def generate_post(user_id: int) -> dict:
    # Impression data schema:
    # [{'id': 1,
    #   'created_at': '2023-01-21T22:09:53+00:00',
    #   'tweet_id': 1,
    #   'user_id': 1,
    #   'child_like_count': 1,
    #   'liked': True}]
    impressions = (
        supabase.table(IMPRESSION_TABLE_NAME).select("*").filter(IMPRESSION_TABLE_USER_ID, "eq", user_id).execute().data
    )
    weights = compute_weights(impressions)
    examples = choose_examples(weights)
    tweet = generate_tweet_from_examples(examples)
    # Tweet data schema:
    # [{'id': 6,
    #   'created_at': '2023-01-21T22:54:52.770345+00:00',
    #   'content': 'insert',
    #   'author': 'test2',
    #   'metadata': {'prompt_example_tweet_ids': [1, 2, 3]}}]
    insert_resp = supabase.table(TWEET_TABLE_NAME).insert(tweet).execute().data[0]
    return {
        TWEET_TABLE_ID: insert_resp[TWEET_TABLE_ID],
        TWEET_TABLE_AUTHOR: insert_resp[TWEET_TABLE_AUTHOR],
        TWEET_TABLE_CONTENT: insert_resp[TWEET_TABLE_CONTENT]
    }


def compute_weights(impressions: List[dict]) -> dict:
    return {i[TWEET_TABLE_ID]: i[IMPRESSION_TABLE_CHILD_LIKE_COUNT] for i in impressions}


def choose_examples(weights: dict) -> dict:
    return {1: "x_user: example 1", 2: "y_user: example 2"}


def generate_tweet_from_examples(examples: dict) -> dict:
    return {
        TWEET_TABLE_CONTENT: "foo",
        TWEET_TABLE_AUTHOR: "foo",
        TWEET_TABLE_METADATA: {METADATA_PROMPT_TWEET_IDS: [1, 2]}
    }
