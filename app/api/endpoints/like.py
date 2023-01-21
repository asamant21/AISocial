"""Endpoints for generating tweets."""

from fastapi import APIRouter

from app.config import supabase
from app.constants import METADATA_PROMPT_TWEET_IDS, IMPRESSION_TABLE_CHILD_LIKE_COUNT, \
    IMPRESSION_TABLE_ID, IMPRESSION_TABLE_NAME

router = APIRouter()


@router.get("/{tweet_id}")
def like(tweet_id: int):
    """Like a tweet by id."""
    user_id = 1
    direct_impression = {"tweet_id": tweet_id, "user_id": user_id, "liked": "true"}
    insert_resp = supabase.table("Impression").insert(direct_impression).execute()
    assert len(insert_resp.data) > 0

    tweet = (
        supabase.table("Tweet").select("*").filter("id", "eq", tweet_id).execute().data[0]
    )
    prompt_examples = tweet["metadata"][METADATA_PROMPT_TWEET_IDS]
    for prompt_tweet_id in prompt_examples:
        existing_impression = (
            supabase.table("Impression")
                .select("*")
                .filter("user_id", "eq", user_id)
                .filter("tweet_id", "eq", tweet_id)
                .execute()
                .data
        )
        if len(existing_impression) == 0:
            new_impression = {
                "user_id": user_id,
                "tweet_id": prompt_tweet_id,
                IMPRESSION_TABLE_CHILD_LIKE_COUNT: 1
            }
            insert_resp = supabase.table(IMPRESSION_TABLE_NAME).insert(new_impression).execute().data
            assert len(insert_resp) > 0
        elif len(existing_impression) == 1:
            count = existing_impression[0][IMPRESSION_TABLE_CHILD_LIKE_COUNT]
            impression_id = existing_impression[0][IMPRESSION_TABLE_ID]
            update_resp = (
                supabase.table("Impression")
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


