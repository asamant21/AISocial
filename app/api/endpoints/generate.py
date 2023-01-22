"""Endpoints for generating tweets."""
from typing import List
import numpy as np
from datetime import datetime
import json
from endpoints.prompts import eg_prompt, prefix, suffix, day_quote

from fastapi import APIRouter
from langchain.llms import OpenAI


from app.api import schemas
from app.config import supabase
from app.constants import TWEET_METADATA_PROMPT_TWEET_IDS, IMPRESSION_TABLE_CHILD_LIKE_COUNT, \
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
        supabase.table(IMPRESSION_TABLE_NAME)
            .select("*")
            .filter(IMPRESSION_TABLE_USER_ID, "eq", user_id)
            .execute()
            .data
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
    weight_dict: dict = {}
    total_weight_sum = sum(
        [impression["child_like_count"] + (10*int(impression["liked"])) for impression in impressions]
    )
    for impression in impressions:
        curr_sum = impression["child_like_count"] + (10*int(impression["liked"]))
        curr_weight = float(curr_sum)/total_weight_sum
        tweet_id = impression["tweet_id"]
        user_id = impression["user_id"]
        id_tuple = f"{tweet_id}, {user_id}"
        weight_dict[id_tuple] = curr_weight

    return weight_dict


def convert_examples(examples: List[str]) -> List[str]:
    tweet_template = """
{{
    tweet": {tweet}
    "user": {user}
}}
    """
    tweet_arr = []
    for example in examples:
        tweet_id, user_id = example.split(", ")
        tweet_str = tweet_template.format(tweet=tweet_id, user=user_id)
        tweet_arr.append(tweet_str)
    return tweet_arr


def choose_examples(weights: dict) -> List[str]:
    weight_list = list(weights.items())
    examples = np.random.choice([weight[0] for weight in weight_list], size=5, p=[weight[1] for weight in weight_list])
    return convert_examples(examples)


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
        "content": loaded_dict["tweet"],
        "author": loaded_dict["user"]
    }
    return return_dict
