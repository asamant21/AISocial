"""Endpoints for generating tweets."""
import json
import random
from datetime import datetime
from typing import List, Optional

import numpy as np
from fastapi import APIRouter, Depends
from langchain.llms import OpenAI
from supabase import Client, create_client

from app.api import deps, schemas
from app.api.db import (
    get_pregenerated_tweet,
    get_seed_impressions,
    get_tweet,
    get_tweet_likes,
    get_user_impressions,
    seed_impressions,
    get_mashed_feed_insight
)
from app.api.endpoints.prompts import (
    day_quote,
    eg_prompt,
    liked_prefix,
    liked_suffix,
    user_spec,
    insight_style_chain,
    better_question_chain,
    insightful_comment_chain
)
from app.config import key, url
from gotrue.types import User
from app.constants import (
    IMPRESSION_TABLE_CHILD_LIKE_COUNT,
    IMPRESSION_TABLE_LIKED,
    IMPRESSION_TABLE_TWEET_ID,
    TWEET_METADATA_PROMPT_TWEET_IDS,
    TWEET_TABLE_AUTHOR,
    TWEET_TABLE_CONTENT,
    TWEET_TABLE_ID,
    TWEET_TABLE_METADATA,
    DEFAULT_STYLE,
    QUESTION_STYLE,
    INSIGHTFUL_STYLE,
    TWEET_TABLE_NAME,
    SUMMARY_TABLE_SYNTHESIS,
    SUMMARY_TABLE_MAIN_SUMMARY,
    TWEET_METADATA_ORIGIN_USER_NUM
)

router = APIRouter()


@router.get("", response_model=schemas.Tweet)
def generate(
    current_user: User = Depends(deps.get_current_user),
    regen_time: datetime = Depends(deps.get_regen_time),
):
    """Generate a tweet for the user."""
    print(current_user)
    return generate_post(current_user, regen_time)


def generate_post(current_user: User, regen_time: datetime = datetime.min) -> dict:
    user_id = str(current_user.id)
    user_num = current_user.user_metadata.get("phone", "")
    user_style = current_user.user_metadata.get("style", DEFAULT_STYLE)
    print(f"User number: {user_num}")

    supabase: Client = create_client(url, key)
    impressions = get_user_impressions(user_id, regen_time)
    if len(impressions) == 0:
        seed_impressions(current_user)
        impressions = get_seed_impressions(user_id, regen_time)

    random_val = random.uniform(0, 1)
    use_pregenerated = len(impressions) < 20 and random_val < 0.2
    if use_pregenerated:
        tweet = get_pregenerated_tweet()
        likes = get_tweet_likes(tweet[TWEET_TABLE_ID])
        return {
            "id": tweet[TWEET_TABLE_ID],
            "author": tweet[TWEET_TABLE_AUTHOR],
            "content": tweet[TWEET_TABLE_CONTENT],
            "metadata": tweet[TWEET_TABLE_METADATA],
            "likes": likes,
        }
    else:
        weights = compute_weights(impressions)
        chosen_impressions = choose_impressions(weights, impressions)

        random_val = random.uniform(0, 1)
        use_insights = random_val < 1
        tweet = None
        if use_insights:
            tweet = generate_insight_tweet(chosen_impressions, user_style, user_num)
            print(tweet)

        # If no insights generated from insight tweet, or use_insights not
        # used, then generate a regular tweet
        if tweet is None:
            tweet = generate_tweet_from_impressions(chosen_impressions)
        insert_resp = supabase.table(TWEET_TABLE_NAME).insert(tweet).execute().data[0]
        print(insert_resp)
        return {
            TWEET_TABLE_ID: insert_resp[TWEET_TABLE_ID],
            TWEET_TABLE_AUTHOR: insert_resp[TWEET_TABLE_AUTHOR],
            TWEET_TABLE_CONTENT: insert_resp[TWEET_TABLE_CONTENT],
            TWEET_TABLE_METADATA: insert_resp[TWEET_TABLE_METADATA],
            "likes": 0,
        }


def compute_weights(impressions: List[dict]) -> List[float]:
    """"""
    weights = []
    total_weight_sum = sum(
        [
            impression[IMPRESSION_TABLE_CHILD_LIKE_COUNT]
            + (10 * int(impression[IMPRESSION_TABLE_LIKED]))
            for impression in impressions
        ]
    )
    for impression in impressions:
        curr_sum = impression[IMPRESSION_TABLE_CHILD_LIKE_COUNT] + (
            10 * int(impression[IMPRESSION_TABLE_LIKED])
        )
        weights.append(float(curr_sum) / total_weight_sum)

    return weights


def convert_example(content: str, author: str) -> str:
    tweet_template = """
{{
    "tweet": {tweet}
    "user": {user}
}}
    """
    return tweet_template.format(tweet=content, user=author)


def convert_impressions_to_examples(impressions: List[dict]) -> List[str]:
    examples = []
    for impression in impressions:
        tweet = get_tweet(impression[IMPRESSION_TABLE_TWEET_ID])
        content = tweet[TWEET_TABLE_CONTENT]
        author = tweet[TWEET_TABLE_AUTHOR]
        examples.append(convert_example(content, author))
    return examples


def choose_impressions(weights: List[float], impressions: List[dict]) -> List[dict]:
    chosen_impressions = np.random.choice(impressions, size=2, replace=False, p=weights)
    return chosen_impressions


def choose_proper_synthesis_base(insight: dict) -> str:
    """Choose from summary, insight, or combination."""
    synthesis = insight[SUMMARY_TABLE_SYNTHESIS]
    summary = insight[SUMMARY_TABLE_MAIN_SUMMARY]
    if len(synthesis) == 0:
        return summary
    combined_info = f"{summary}\n{synthesis}"
    return random.choice([synthesis, summary, combined_info])


def generate_insight_tweet(impressions: List[dict], user_style: str = DEFAULT_STYLE, user_num: str = "") -> Optional[dict]:
    """Generate insight twee."""
    num_used, insight = get_mashed_feed_insight(user_num)
    print(num_used)
    # If no insight exist for the current number
    if insight is None:
        return None

    tweets = {}
    for i in range(2):
        try:
            insight = choose_proper_synthesis_base(insight)
            examples = convert_impressions_to_examples(impressions)
            print(insight)

            chain = insight_style_chain
            if user_style == QUESTION_STYLE:
                chain = better_question_chain
            elif user_style == INSIGHTFUL_STYLE:
                chain = insightful_comment_chain
            insights_dict = {"insights": insight, "style_samples": str(examples)}
            insight_transfer = chain(insights_dict)["text"]
            print(insight_transfer)
            tweets = json.loads(insight_transfer)
        except:
            continue

    if len(tweets) == 0:
        return None

    impression_ids = [
        impression[IMPRESSION_TABLE_TWEET_ID] for impression in impressions
    ]

    tweet_metadata = {
        TWEET_METADATA_PROMPT_TWEET_IDS: impression_ids,
    }
    if num_used != user_num:
        tweet_metadata[TWEET_METADATA_ORIGIN_USER_NUM] = num_used

    return_dict = {
        TWEET_TABLE_CONTENT: tweets["tweet"],
        TWEET_TABLE_AUTHOR: tweets["user_name"],
        TWEET_TABLE_METADATA: tweet_metadata,
    }
    return return_dict


def generate_tweet_from_impressions(impressions: List[dict]) -> dict:
    examples = convert_impressions_to_examples(impressions)
    eg = eg_prompt.format(tweets=str(examples))
    day_prefix = day_quote.format(today=str(datetime.today().date()))
    full_prefix = liked_prefix + day_prefix
    full_prompt = full_prefix + eg + liked_suffix + user_spec

    curr_temp = 1.0
    llm = OpenAI(temperature=curr_temp)
    loaded_dict = {}

    for i in range(3):
        try:
            llm.temperature = curr_temp
            gen_tweet = llm(full_prompt)
            stripped_tweet = gen_tweet.strip(",\n")
            loaded_dict = json.loads(stripped_tweet)
            break
        except:
            # Lower the temperature, it could be getting the formatting wrong
            curr_temp /= 2
            continue

    if len(loaded_dict) == 0:
        return loaded_dict

    impression_ids = [
        impression[IMPRESSION_TABLE_TWEET_ID] for impression in impressions
    ]

    return_dict = {
        TWEET_TABLE_CONTENT: loaded_dict["tweet"],
        TWEET_TABLE_AUTHOR: loaded_dict["user"],
        TWEET_TABLE_METADATA: {TWEET_METADATA_PROMPT_TWEET_IDS: impression_ids},
    }
    return return_dict
