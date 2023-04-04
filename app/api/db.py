"""Helper functions for interacting with the database."""
import random
from datetime import datetime, timezone
from typing import List, Optional, Tuple

import requests
from gotrue.types import User
from supabase import Client, create_client

from app.config import key, second_key, second_url, url
from app.constants import (
    DEFAULT_STYLE,
    FRIEND_TABLE_FRIEND_NUM,
    FRIEND_TABLE_NAME,
    FRIEND_TABLE_USER_NUM,
    IMPRESSION_TABLE_CHILD_LIKE_COUNT,
    IMPRESSION_TABLE_CREATED_TIME,
    IMPRESSION_TABLE_ID,
    IMPRESSION_TABLE_LIKED,
    IMPRESSION_TABLE_NAME,
    IMPRESSION_TABLE_TWEET_ID,
    IMPRESSION_TABLE_USER_ID,
    INSIGHTFUL_STYLE,
    INSIGHTFUL_TWEET_IDS,
    INTERESTING_QUESTION_TWEET_IDS,
    QUESTION_STYLE,
    SEED_TWEET_IDS,
    SUPABASE_TRUE_VAL,
    TWEET_TABLE_ID,
    TWEET_TABLE_NAME,
)


def get_seed_impressions(
    user_id: str, regen_time: datetime = datetime.min
) -> List[dict]:
    """Return all seed impressions."""
    supabase: Client = create_client(url, key)
    IDS = SEED_TWEET_IDS
    IDS.extend(INSIGHTFUL_TWEET_IDS)
    IDS.extend(INTERESTING_QUESTION_TWEET_IDS)
    impressions = (
        supabase.table("Impression")
        .select("*")
        .filter(IMPRESSION_TABLE_USER_ID, "eq", user_id)
        .filter(IMPRESSION_TABLE_TWEET_ID, "in", tuple(IDS))
        .filter(IMPRESSION_TABLE_CREATED_TIME, "gt", regen_time)
        .execute()
        .data
    )
    print(impressions)
    return impressions


def get_user_impressions(
    user_id: str, regen_time: datetime = datetime.min
) -> List[dict]:
    """Return all the impressions for a user after a generation time."""
    supabase: Client = create_client(url, key)
    impressions = (
        supabase.table("Impression")
        .select("*")
        .filter(IMPRESSION_TABLE_USER_ID, "eq", user_id)
        .filter(IMPRESSION_TABLE_CREATED_TIME, "gt", regen_time)
        .execute()
        .data
    )
    return impressions


def seed_impressions(user: User) -> None:
    """Add initial impressions for a new user."""
    user_id = user.id
    user_style = user.user_metadata.get("style", DEFAULT_STYLE)
    supabase: Client = create_client(url, key)

    OTHER_TWEETS_TO_SAMPLE_FROM = [INSIGHTFUL_TWEET_IDS, INTERESTING_QUESTION_TWEET_IDS]
    BASE_TWEET_TO_SAMPLE = SEED_TWEET_IDS
    print(f"USER STYLE: {user_style}")

    if user_style == INSIGHTFUL_STYLE:
        BASE_TWEET_TO_SAMPLE = INSIGHTFUL_TWEET_IDS
        OTHER_TWEETS_TO_SAMPLE_FROM = [INTERESTING_QUESTION_TWEET_IDS]
    elif user_style == QUESTION_STYLE:
        BASE_TWEET_TO_SAMPLE = INTERESTING_QUESTION_TWEET_IDS
        OTHER_TWEETS_TO_SAMPLE_FROM = []

    tweets_to_use = random.sample(BASE_TWEET_TO_SAMPLE, k=20)
    # Add 5 more tweets from the other options
    for alternate_tweets_list in OTHER_TWEETS_TO_SAMPLE_FROM:
        alternate_tweets = random.sample(alternate_tweets_list, k=5)
        tweets_to_use.extend(alternate_tweets)

    for tweet_id in tweets_to_use:
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
    supabase: Client = create_client(url, key)
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
    user_impression = get_impression(tweet_id, user_id)[0]
    likes = get_tweet_likes(tweet_id)
    return {**tweet, "liked": user_impression[IMPRESSION_TABLE_LIKED], "likes": likes}


def get_user_liked_tweets(user_id: str) -> List[dict]:
    """Retrieve all tweets liked by a user."""
    like_impressions = get_user_like_impressions(user_id)
    tweet_ids = [i[IMPRESSION_TABLE_TWEET_ID] for i in like_impressions]
    user_tweet_views = [get_user_tweet_view(tid, user_id) for tid in tweet_ids]
    return user_tweet_views


def get_user_like_impressions(user_id: str) -> List[dict]:
    """Get all direct like impressions for a user."""
    supabase: Client = create_client(url, key)
    impressions = (
        supabase.table(IMPRESSION_TABLE_NAME)
        .select("*")
        .filter(IMPRESSION_TABLE_USER_ID, "eq", user_id)
        .filter(IMPRESSION_TABLE_LIKED, "eq", SUPABASE_TRUE_VAL)
        .execute()
        .data
    )
    return impressions


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
    supabase: Client = create_client(url, key)
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
    supabase: Client = create_client(url, key)
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
    supabase: Client = create_client(url, key)
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
    supabase: Client = create_client(url, key)
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
    supabase: Client = create_client(url, key)
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


def get_all_friends(user_num: str) -> List[dict]:
    """Get all friends of a user."""
    supabase: Client = create_client(second_url, second_key)
    friends = (
        supabase.table(FRIEND_TABLE_NAME)
        .select("*")
        .filter(FRIEND_TABLE_USER_NUM, "eq", user_num)
        .execute()
        .data
    )
    return friends


def get_mashed_feed_insight(user_num: str) -> Tuple[str, Optional[dict]]:
    """Get an insight from you or one of your friends.

    First choose a random insight from either you or your friend. If nothing
    comes from your friend, choose one for you.
    """
    friends = get_all_friends(user_num)
    friend_nums = [friend[FRIEND_TABLE_FRIEND_NUM] for friend in friends]
    all_nums = friend_nums + [user_num]
    print(all_nums)

    num_to_use = random.choice(all_nums)
    insight = get_random_insight(num_to_use)

    if num_to_use != user_num and insight is None:
        return user_num, get_random_insight(user_num)

    return num_to_use, insight


def get_random_insight(user_num: str) -> Optional[dict]:
    """Get random insight from user num provided."""
    user_num = user_num.replace("+", "%2B")
    token = f"Bearer {second_key}"
    request_url = f"{second_url}/rest/v1/rpc/get_random_summary?number={user_num}"
    res = requests.request(
        "GET", request_url, headers={"Authorization": token, "apikey": second_key}
    )

    vals = res.json()
    print(vals)
    # No insight for the existing number
    if len(vals) > 0:
        return vals[0]
    return None
