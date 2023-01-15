from typing import Dict, List
import numpy as np
from aisocial.Topic.base import BaseTopic
from aisocial.Topic.generate import format_topics_for_prompt, generate_topics

topic_cache: Dict[str, BaseTopic] = {}
MAX_TOPICS = 3
USER_REC_ADJUSTMENT = 2


def construct_topic_probability_dist(topics: List[BaseTopic]) -> List[float]:
    """Construct topic probability distribution."""
    total_rec_sum = sum([topic.recommendation_rating for topic in topics])
    return [(topic.recommendation_rating/total_rec_sum) for topic in topics]


def retrieve_seed_topics() -> List[BaseTopic]:
    """Retrieve list of seed topics for feeding to LLMs."""
    # TODO: make this smarter
    topics = list(topic_cache.values())
    topics = sorted(
        topics, key=lambda topic: topic.recommendation_rating, reverse=True
    )
    probability_dist = construct_topic_probability_dist(topics)
    select_size = min(len(topics), MAX_TOPICS)
    return list(np.random.choice(topics, size=select_size, replace=False, p=probability_dist))


def add_user_recommended_topics(user_topics: List[str]) -> None:
    """Seed topic cache with user provided topics."""
    user_topics = [topic.lower() for topic in user_topics]
    for topic_name in user_topics:
        if topic_name in topic_cache:
            topic = topic_cache[topic_name]
            if topic.user_provided:
                continue

            new_topic = topic.copy()
            new_topic.user_provided = True
            new_topic.update_rec_rating(USER_REC_ADJUSTMENT)
        else:
            new_topic = BaseTopic(
                name=topic_name,
                user_provided=True,
                recommendation_rating=USER_REC_ADJUSTMENT,
            )

        topic_cache[topic_name] = new_topic


def generate_new_topics() -> None:
    seed_topics = retrieve_seed_topics()
    new_topics = generate_topics(seed_topics)
    for new_topic in new_topics:
        if new_topic.name in topic_cache:
            topic = topic_cache.get(new_topic.name)
            topic.update_rec_rating(1)
            topic_cache.update({topic.name: topic})
        else:
            topic_cache[new_topic.name] = new_topic
