"""Endpoints for generating tweets."""
from typing import List
import numpy as np
from datetime import datetime
import json

from fastapi import APIRouter, Depends
from langchain.llms import OpenAI

from app.api import deps, schemas
from app.api.db import get_user_impressions, seed_impressions, get_tweet, \
    get_tweet_likes
from app.config import supabase
from app.constants import (
    TWEET_TABLE_ID,
    TWEET_TABLE_AUTHOR, TWEET_TABLE_CONTENT, TWEET_TABLE_NAME,
    IMPRESSION_TABLE_TWEET_ID, IMPRESSION_TABLE_CHILD_LIKE_COUNT, IMPRESSION_TABLE_LIKED
)
from app.api.endpoints.prompts import eg_prompt, prefix, suffix, day_quote

router = APIRouter()


@router.get("", response_model=schemas.Tweet)
def generate(current_user: str = Depends(deps.get_current_user)):
    """Generate a tweet for the user."""
    print(current_user)
    return generate_post(current_user)


def generate_post(user_id: str) -> dict:
    impressions = get_user_impressions(user_id)
    if len(impressions) == 0:
        seed_impressions(user_id)
    use_pregenerated = False
    if use_pregenerated:
        tweet = {}  # get_existing_tweet()
        likes = get_tweet_likes(tweet[TWEET_TABLE_ID])
        return {
            "id": tweet[TWEET_TABLE_ID],
            "author": tweet[TWEET_TABLE_AUTHOR],
            "content": tweet[TWEET_TABLE_CONTENT],
            "likes": likes
        }
    else:
        weights = compute_weights(impressions)
        examples = choose_examples(weights, impressions)
        tweet = generate_tweet_from_examples(examples)
        insert_resp = supabase.table(TWEET_TABLE_NAME).insert(tweet).execute().data[0]
        return {
            "id": insert_resp[TWEET_TABLE_ID],
            "author": insert_resp[TWEET_TABLE_AUTHOR],
            "content": insert_resp[TWEET_TABLE_CONTENT],
            "likes": 0,
        }


def compute_weights(impressions: List[dict]) -> List[float]:
    """"""
    weights = []
    total_weight_sum = sum(
        [impression[IMPRESSION_TABLE_CHILD_LIKE_COUNT] + (10 * int(impression[IMPRESSION_TABLE_LIKED])) for impression in impressions]
    )
    for impression in impressions:
        curr_sum = impression[IMPRESSION_TABLE_CHILD_LIKE_COUNT] + (10*int(impression[IMPRESSION_TABLE_LIKED]))
        weights.append(float(curr_sum)/total_weight_sum)

    return weights


def convert_example(content: str, author: str) -> str:
    tweet_template = """
{{
    "tweet": {tweet}
    "user": {user}
}}
    """
    return tweet_template.format(tweet=content, user=author)


def choose_examples(weights: List[float], impressions: List[dict]) -> List[str]:
    examples = []
    chosen_impressions = np.random.choice(impressions, size=5, p=weights)
    for impression in chosen_impressions:
        tweet = get_tweet(impression[IMPRESSION_TABLE_TWEET_ID])
        content = tweet[TWEET_TABLE_CONTENT]
        author = tweet[TWEET_TABLE_AUTHOR]
        examples.append(convert_example(content, author))
    return examples


def generate_tweet_from_examples(examples: List[str]) -> dict:
    eg = eg_prompt.format(tweets=("\n".join(examples)))
    day_prefix = day_quote.format(today=str(datetime.today().date()))
    full_prefix = prefix + f"\n{day_prefix}"
    full_prompt = full_prefix + eg + suffix
    llm = OpenAI(temperature=1)

    loaded_dict = {}

    curr_temp = 1
    for i in range(3):
        try:
            llm.temperature = curr_temp
            gen_tweet = llm(full_prompt)
            stripped_tweet = gen_tweet.strip("\n ")
            loaded_dict = json.loads(stripped_tweet)
            break
        except:
            # Lower the temperature, it could be getting the formatting wrong
            curr_temp /= 2
            continue

    if len(loaded_dict) == 0:
        return loaded_dict

    return_dict = {
        TWEET_TABLE_CONTENT: loaded_dict["tweet"],
        TWEET_TABLE_AUTHOR: loaded_dict["user"]
    }
    return return_dict
