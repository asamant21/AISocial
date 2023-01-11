import uuid
from datetime import datetime
from typing import Dict, List

import openai

from aisocial import chain
from aisocial.Post.base import BasePost
from aisocial.Post.generate import generate_image_prompt, parse_tweet
from aisocial.Post.image import ImagePost
from aisocial.Post.prompts import TWEET_TEMPL
from aisocial.Post.text import TextPost
from aisocial.Topic import BaseTopic

post_cache: Dict[str, BasePost] = {}
__all__ = ["TextPost", "ImagePost"]


def generate_text_post(topics: List[BaseTopic]) -> TextPost:
    """Generate a Text Post and add it to the cache."""
    seed_topic_names = [topic.name for topic in topics]
    formatted_topics = ", ".join(seed_topic_names)
    tweet_question = TWEET_TEMPL.format(topics=formatted_topics)
    llm_output = chain(inputs={"question": tweet_question})["text"]
    used_topics, tweet = parse_tweet(llm_output)

    diff_topics = set(used_topics) - set(seed_topic_names)
    if len(diff_topics) > 0:
        raise ValueError(f"Topics {diff_topics} unexpected")

    post_id = str(uuid.uuid4())
    text_post = TextPost(
        post_id=post_id,
        topics=used_topics,
        content=tweet,
        created_time=datetime.now(),
    )
    post_cache[post_id] = text_post
    return text_post


def generate_image_post(topics: List[BaseTopic]) -> ImagePost:
    """Generate image post and add it to the cache."""
    image_prompt = generate_image_prompt(topics)
    topic_names = [topic.name for topic in topics]
    response = openai.Image.create(
        prompt=image_prompt,
        n=1,
        size="256x256",
    )

    response_url = response["data"][0]["url"]

    post_id = str(uuid.uuid4())
    image_post = ImagePost(
        post_id=post_id,
        topics=topic_names,
        content=response_url,
        created_time=datetime.now(),
        prompt=image_prompt,
    )
    post_cache[post_id] = image_post
    return image_post