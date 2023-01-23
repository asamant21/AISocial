"""Helper functions for interacting with the database."""
from typing import List

import requests

from app.config import key, supabase, url
from app.constants import (
    IMPRESSION_TABLE_CHILD_LIKE_COUNT,
    IMPRESSION_TABLE_ID,
    IMPRESSION_TABLE_LIKED,
    IMPRESSION_TABLE_NAME,
    IMPRESSION_TABLE_TWEET_ID,
    IMPRESSION_TABLE_USER_ID,
    SEED_TWEET_IDS,
    SUPABASE_TRUE_VAL,
    TWEET_TABLE_ID,
    TWEET_TABLE_NAME,
)


def get_user_impressions(user_id: str) -> List[dict]:
    """Return all the impressions for a user."""
    impressions = (
        supabase.table(IMPRESSION_TABLE_NAME)
        .select("*")
        .filter(IMPRESSION_TABLE_USER_ID, "eq", user_id)
        .execute()
        .data
    )
    return impressions


def seed_impressions(user_id: str) -> None:
    """Add initial impressions for a new user."""
    for tweet_id in SEED_TWEET_IDS:
        impression = {
            IMPRESSION_TABLE_USER_ID: user_id,
            IMPRESSION_TABLE_TWEET_ID: tweet_id,
            IMPRESSION_TABLE_CHILD_LIKE_COUNT: 1,
        }
        insert_resp = (
            supabase.table(IMPRESSION_TABLE_NAME).insert(impression).execute().data
        )
        assert len(insert_resp) > 0


def get_tweet(tweet_id: int) -> dict:
    """Retrieve tweet based on id."""
    tweet = (
        supabase.table(TWEET_TABLE_NAME)
        .select("*")
        .filter(TWEET_TABLE_ID, "eq", tweet_id)
        .execute()
        .data[0]
    )
    return tweet


def get_user_tweet_view(tweet_id: int, user_id: str) -> dict:
    """Retrieve a tweet along with liked status for the current user and total likes."""
    tweet = get_tweet(tweet_id)
    user_impression = get_impression(tweet_id, user_id)
    likes = get_tweet_likes(tweet_id)
    return {**tweet, "liked": user_impression[IMPRESSION_TABLE_LIKED], "likes": likes}


def get_pregenerated_tweet() -> dict:
    """"""
    token = f"Bearer {key}"
    request_url = f"{url}/rest/v1/rpc/get_random_tweet"
    res = requests.request(
        "GET", request_url, headers={"Authorization": token, "apikey": key}
    )
    return res.json()[0]


def get_tweet_likes(tweet_id: int) -> int:
    """Retrieve number of direct tweet likes."""
    likes = (
        supabase.table(IMPRESSION_TABLE_NAME)
        .select("*")
        .filter(IMPRESSION_TABLE_TWEET_ID, "eq", tweet_id)
        .filter(IMPRESSION_TABLE_LIKED, "eq", SUPABASE_TRUE_VAL)
        .execute()
        .data
    )
    return len(likes)


def add_direct_impression(tweet_id: int, user_id: str) -> None:
    """Add an impression of a direct tweet like."""
    direct_impression = {
        IMPRESSION_TABLE_TWEET_ID: tweet_id,
        IMPRESSION_TABLE_USER_ID: user_id,
        IMPRESSION_TABLE_LIKED: SUPABASE_TRUE_VAL,
    }
    insert_resp = (
        supabase.table(IMPRESSION_TABLE_NAME).insert(direct_impression).execute().data
    )
    assert len(insert_resp) > 0


def get_impression(tweet_id: int, user_id: str) -> dict:
    """Retrieve impression based on tweet and user id."""
    impression = (
        supabase.table(IMPRESSION_TABLE_NAME)
        .select("*")
        .filter(IMPRESSION_TABLE_USER_ID, "eq", user_id)
        .filter(IMPRESSION_TABLE_TWEET_ID, "eq", tweet_id)
        .execute()
        .data
    )
    return impression


def add_prompt_impression(tweet_id: int, user_id: str) -> None:
    """Add impression for a prompt tweet after a derived tweet was liked."""
    impression = {
        IMPRESSION_TABLE_USER_ID: user_id,
        IMPRESSION_TABLE_TWEET_ID: tweet_id,
        IMPRESSION_TABLE_CHILD_LIKE_COUNT: 1,
    }
    insert_resp = (
        supabase.table(IMPRESSION_TABLE_NAME).insert(impression).execute().data
    )
    assert len(insert_resp) > 0


def update_prompt_impression(impression: dict) -> None:
    """Update existing impression for a prompt tweet after a derived tweet was liked."""
    count = impression[IMPRESSION_TABLE_CHILD_LIKE_COUNT]
    impression_id = impression[IMPRESSION_TABLE_ID]
    update_resp = (
        supabase.table(IMPRESSION_TABLE_NAME)
        .update({IMPRESSION_TABLE_CHILD_LIKE_COUNT: count + 1})
        .filter(IMPRESSION_TABLE_ID, "eq", impression_id)
        .execute()
        .data
    )
    assert len(update_resp) > 0
