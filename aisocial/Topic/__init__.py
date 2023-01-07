from aisocial.Topic.base import BaseTopic
from aisocial.Topic.generate import generate_topics, format_topics_for_prompt
from typing import Dict, List

topic_cache: Dict[str, BaseTopic] = {}
MAX_TOPICS = 10
USER_REC_ADJUSTMENT = 2


def retrieve_seed_topics() -> List[BaseTopic]:
    """Retrieve list of seed topics for feeding to LLMs."""
    # TODO: make this smarter
    topics = list(topic_cache.values())
    seed_topics = sorted(
        topics,
        key=lambda topic: topic.recommendation_rating,
        reverse=True
    )
    return seed_topics[:MAX_TOPICS]


def add_user_recommended_topics(user_topics: List[str]) -> None:
    """Seed topic cache with user provided topics."""
    for topic_name in user_topics:
        if topic_name in topic_cache:
            topic = topic_cache[topic_name]
            if topic.user_provided:
                raise ValueError(f"Already recommended topic {topic_name}")

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