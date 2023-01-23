"""Endpoints for liking tweets."""

from fastapi import APIRouter, Depends

from app.api import deps
from app.api.db import get_tweet, add_direct_impression, get_impression, \
    add_prompt_impression, update_prompt_impression
from app.constants import TWEET_METADATA_PROMPT_TWEET_IDS, IMPRESSION_TABLE_NAME, \
    TWEET_TABLE_METADATA

router = APIRouter()


@router.get("/{tweet_id}")
def like(tweet_id: int, current_user: str = Depends(deps.get_current_user), level: int = 0):
    """Like a tweet by id."""
    if level > 1:
        return

    impression = get_impression(tweet_id, current_user)

    if len(impression) > 1:
        raise ValueError(
            f"Duplicate user <> tweet impression stored in {IMPRESSION_TABLE_NAME}"
            f" table."
        )

    if len(impression) == 0 and level == 0:
        add_direct_impression(tweet_id, current_user)
    elif len(impression) == 0:
        add_prompt_impression(tweet_id, current_user)
    else:
        update_prompt_impression(impression[0])

    tweet = get_tweet(tweet_id)
    metadata = tweet.get(TWEET_TABLE_METADATA)

    if metadata is None:
        return
    prompt_examples = metadata.get(TWEET_METADATA_PROMPT_TWEET_IDS, {})
    for prompt_tweet_id in prompt_examples:
        like(prompt_tweet_id, current_user, level+1)
