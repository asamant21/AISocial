"""File that generates recommendations based on a past history."""
from typing import List
import re

from aisocial.Post.prompts import (
    IMAGE_PROMPT_TEMPL_BASE,
    IMAGE_PROMPT_TEMPL_END
)
from aisocial import clean_parsed_output, chain
from aisocial.Topic.base import BaseTopic
from aisocial.Topic import (
    format_topics_for_prompt,
)


def generate_image_prompt(topics: List[BaseTopic]) -> str:
    """Generate image prompt."""
    formatted_topics = format_topics_for_prompt(topics)
    image_base = IMAGE_PROMPT_TEMPL_BASE.format(topics=formatted_topics)
    image_question = image_base+IMAGE_PROMPT_TEMPL_END
    llm_response = chain(inputs={"question": image_question})
    return parse_image_rec_to_prompt(llm_response["text"])


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