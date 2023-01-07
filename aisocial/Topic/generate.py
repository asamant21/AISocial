"""Helpers for generating and choosing topics."""
from typing import List

from langchain.chains import LLMChain
from langchain.llms import OpenAI

import aisocial
from aisocial.Topic.base import BaseTopic

llm = OpenAI(
    model_name="text-davinci-003",
    temperature=1.0,
    openai_api_key=aisocial.OPENAI_API_KEY,
)
chain = LLMChain(llm=llm, prompt=aisocial.BASE_PROMPT)

# Temperature = 1.0
EXTRA_TOPICS_TEMPL = """
You are a cultural tastemaker curating topics for an individual. You take risks and are not afraid to try new things.
You will be provided information about a person and your task is to output a list of topics that the person would enjoy
learning about.

The topics can be related or entirely different. The choice is yours. You should not be afraid to
suggest unorthodox or unexpected topics, but your recommendations should not only consist of these. 
Each topic can be a person, a thing, a style, a subject, an activity. Don't limit yourself. Be specific. 
Each topic should be one word.

Below is a list of topics that the person likes:
{topics}

Use the following format:
[Topic 1 that user can find interesting, ... , Topic 5 that user can find interesting]

Remember, you should be specific and draw from many different sources when making suggestions.
Don't limit yourself.
Begin!
"""


def parse_llm_topic_output(llm_output: str) -> List[BaseTopic]:
    """Parse llm topic output to list of topics."""
    llm_output = llm_output.strip()
    llm_output = llm_output.strip("[]")
    topic_names = llm_output.split(",")

    topic_list = []
    for topic_name in topic_names:
        topic_name = topic_name.strip()
        topic = BaseTopic(name=topic_name)
        topic_list.append(topic)

    return topic_list


def generate_topics(seed_topics: List[BaseTopic]) -> List[BaseTopic]:
    formatted_topics = format_topics_for_prompt(seed_topics)
    topics_questions = EXTRA_TOPICS_TEMPL.format(topics=formatted_topics)
    llm_response = chain(inputs={"question": topics_questions})
    return parse_llm_topic_output(llm_response["text"])


def format_topics_for_prompt(topics: List[BaseTopic]) -> str:
    """Formats list of topics into a string"""
    final_str = ""
    for id, topic in enumerate(topics):
        final_str += f"{id+1}. {topic.name}\n"
    return final_str
