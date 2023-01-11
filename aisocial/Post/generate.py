"""File that generates recommendations based on a past history."""
import re
from typing import List, Tuple

from aisocial import chain, clean_parsed_output
from aisocial.Post.prompts import (IMAGE_PROMPT_TEMPL_BASE,
                                   IMAGE_PROMPT_TEMPL_END)
from aisocial.Topic import format_topics_for_prompt
from aisocial.Topic.base import BaseTopic


def generate_image_prompt(topics: List[BaseTopic]) -> str:
    """Generate image prompt."""
    formatted_topics = format_topics_for_prompt(topics)
    image_base = IMAGE_PROMPT_TEMPL_BASE.format(topics=formatted_topics)
    image_question = image_base + IMAGE_PROMPT_TEMPL_END
    llm_response = chain(inputs={"question": image_question})
    return parse_image_rec_to_prompt(llm_response["text"])


def parse_tweet(llm_output: str) -> Tuple[List[str], str]:
    """Parse tweet prompt output to tweet + topics."""
    llm_output = llm_output.strip()
    regex = r"TOPICS: (.*?)\n*TWEET: (.*)"
    match = re.search(regex, llm_output, re.I)
    if not match:
        raise ValueError(f"Could not parse LLM output: `{llm_output}`")

    topics = clean_parsed_output(match.group(1))
    topics_list = topics.split(",")
    tweet = clean_parsed_output(match.group(2))
    topic_names = [clean_parsed_output(topic).lower() for topic in topics_list]

    return topic_names, tweet


def parse_image_rec_to_prompt(llm_output: str) -> str:
    """Parses image prompt output to DALLE prompt."""
    llm_output = llm_output.strip()
    regex = r"Description: (.*?)\n*Style: (.*)\n*Artist References: (.*)"
    match = re.search(regex, llm_output)
    if not match:
        raise ValueError(f"Could not parse LLM output: `{llm_output}`")
    description = clean_parsed_output(match.group(1))
    style = clean_parsed_output(match.group(2))
    artist_references = clean_parsed_output(match.group(3))

    combined_prompt = ". ".join([description, style, artist_references]) + "."
    return combined_prompt
