"""Endpoints for generating tweets."""

from fastapi import APIRouter

from app.config import supabase
from app.constants import METADATA_PROMPT_TWEET_IDS, IMPRESSION_TABLE_CHILD_LIKE_COUNT, \
    IMPRESSION_TABLE_ID, IMPRESSION_TABLE_NAME, IMPRESSION_TABLE_USER_ID, \
    IMPRESSION_TABLE_TWEET_ID, TWEET_TABLE_METADATA, IMPRESSION_TABLE_LIKED, \
    TWEET_TABLE_NAME, SUPABASE_TRUE_VAL, TWEET_TABLE_ID

router = APIRouter()


@router.get("/{tweet_id}")
def like(tweet_id: int):
    """Like a tweet by id."""
    user_id = 1
    direct_impression = {IMPRESSION_TABLE_TWEET_ID: tweet_id, IMPRESSION_TABLE_USER_ID: user_id, IMPRESSION_TABLE_LIKED: SUPABASE_TRUE_VAL}
    insert_resp = supabase.table(IMPRESSION_TABLE_NAME).insert(direct_impression).execute()
    assert len(insert_resp.data) > 0

    tweet = (
        supabase.table(TWEET_TABLE_NAME).select("*").filter(TWEET_TABLE_ID, "eq", tweet_id).execute().data[0]
    )
    prompt_examples = tweet[TWEET_TABLE_METADATA][METADATA_PROMPT_TWEET_IDS]
    for prompt_tweet_id in prompt_examples:
        existing_impression = (
            supabase.table(IMPRESSION_TABLE_NAME)
                .select("*")
                .filter(IMPRESSION_TABLE_USER_ID, "eq", user_id)
                .filter(IMPRESSION_TABLE_TWEET_ID, "eq", tweet_id)
                .execute()
                .data
        )
        if len(existing_impression) == 0:
            new_impression = {
                IMPRESSION_TABLE_USER_ID: user_id,
                IMPRESSION_TABLE_TWEET_ID: prompt_tweet_id,
                IMPRESSION_TABLE_CHILD_LIKE_COUNT: 1
            }
            insert_resp = supabase.table(IMPRESSION_TABLE_NAME).insert(new_impression).execute().data
            assert len(insert_resp) > 0
        elif len(existing_impression) == 1:
            count = existing_impression[0][IMPRESSION_TABLE_CHILD_LIKE_COUNT]
            impression_id = existing_impression[0][IMPRESSION_TABLE_ID]
            update_resp = (
                supabase.table(IMPRESSION_TABLE_NAME)
                    .update({IMPRESSION_TABLE_CHILD_LIKE_COUNT: count + 1})
                    .filter(IMPRESSION_TABLE_ID, "eq", impression_id)
                    .execute()
                    .data
            )
            assert len(update_resp) > 0
        else:
            raise ValueError(
                "Duplicate user <> tweet impression stored in Impression table."
            )
        assert len(insert_resp.data) > 0


