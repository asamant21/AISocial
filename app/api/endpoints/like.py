"""Endpoints for liking tweets."""

from fastapi import APIRouter, Depends

from app.api import deps
from app.api.db import get_tweet, add_direct_impression, get_impression, \
    add_prompt_impression, update_prompt_impression
from app.constants import TWEET_METADATA_PROMPT_TWEET_IDS, IMPRESSION_TABLE_NAME, \
    TWEET_TABLE_METADATA

router = APIRouter()


@router.get("/{tweet_id}")
def like(tweet_id: int, current_user: str = Depends(deps.get_current_user)):
    """Like a tweet by id."""
    add_direct_impression(tweet_id, current_user)
    tweet = get_tweet(tweet_id)
    prompt_examples = tweet[TWEET_TABLE_METADATA][TWEET_METADATA_PROMPT_TWEET_IDS]
    for prompt_tweet_id in prompt_examples:
        existing_impression = get_impression(prompt_tweet_id, current_user)
        if len(existing_impression) == 0:
            add_prompt_impression(prompt_tweet_id, current_user)
        elif len(existing_impression) == 1:
            update_prompt_impression(existing_impression[0])
        else:
            raise ValueError(
                f"Duplicate user <> tweet impression stored in {IMPRESSION_TABLE_NAME}"
                f" table."
            )


