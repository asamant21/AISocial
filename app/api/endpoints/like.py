"""Endpoints for generating tweets."""

from fastapi import APIRouter, Depends

from app.config import supabase
from app.constants import TWEET_METADATA_PROMPT_TWEET_IDS, IMPRESSION_TABLE_CHILD_LIKE_COUNT, \
    IMPRESSION_TABLE_ID, IMPRESSION_TABLE_NAME, IMPRESSION_TABLE_USER_ID, \
    IMPRESSION_TABLE_TWEET_ID, TWEET_TABLE_METADATA, IMPRESSION_TABLE_LIKED, \
    TWEET_TABLE_NAME, SUPABASE_TRUE_VAL, TWEET_TABLE_ID
from app.api import deps
router = APIRouter()


@router.get("/{tweet_id}")
def like(tweet_id: int, current_user: str = Depends(deps.get_current_user)):
    """Like a tweet by id."""
    user_id = 1
    add_direct_impression(tweet_id, user_id)
    tweet = get_tweet(tweet_id)
    prompt_examples = tweet[TWEET_TABLE_METADATA][TWEET_METADATA_PROMPT_TWEET_IDS]
    for prompt_tweet_id in prompt_examples:
        existing_impression = get_impression(tweet_id, user_id)
        if len(existing_impression) == 0:
            add_prompt_impression(prompt_tweet_id, user_id)
        elif len(existing_impression) == 1:
            update_prompt_impression(existing_impression[0])
        else:
            raise ValueError(
                f"Duplicate user <> tweet impression stored in {IMPRESSION_TABLE_NAME}"
                f" table."
            )


def add_direct_impression(tweet_id: int, user_id: int) -> None:
    """"""
    direct_impression = {
        IMPRESSION_TABLE_TWEET_ID: tweet_id,
        IMPRESSION_TABLE_USER_ID: user_id,
        IMPRESSION_TABLE_LIKED: SUPABASE_TRUE_VAL
    }
    insert_resp = (
        supabase.table(IMPRESSION_TABLE_NAME).insert(direct_impression).execute().data
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


def get_impression(tweet_id: int, user_id: int) -> dict:
    """"""
    impression = (
        supabase.table(IMPRESSION_TABLE_NAME)
            .select("*")
            .filter(IMPRESSION_TABLE_USER_ID, "eq", user_id)
            .filter(IMPRESSION_TABLE_TWEET_ID, "eq", tweet_id)
            .execute()
            .data
    )
    return impression


def add_prompt_impression(tweet_id: int, user_id: int) -> None:
    impression = {
        IMPRESSION_TABLE_USER_ID: user_id,
        IMPRESSION_TABLE_TWEET_ID: tweet_id,
        IMPRESSION_TABLE_CHILD_LIKE_COUNT: 1
    }
    insert_resp = supabase.table(IMPRESSION_TABLE_NAME).insert(
        impression).execute().data
    assert len(insert_resp) > 0


def update_prompt_impression(impression: dict) -> None:
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
