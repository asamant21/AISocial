"""File that runs main post generation."""
import random

from aisocial.Post import BasePost, generate_image_post, generate_text_post
from aisocial.Topic import retrieve_seed_topics, generate_new_topics


def cull_topics_and_add_new() -> None:
    """Cull caches of stale topics and posts."""


def generate_post() -> BasePost:
    """Generate a post."""
    val = random.uniform(0, 1)
    for i in range(3):
        try:
            if val < 0.5:
                seed_topics = retrieve_seed_topics(3)
                return generate_text_post(seed_topics)
            else:
                seed_topics = retrieve_seed_topics(5)
                return generate_image_post(seed_topics)
        except:
            continue
