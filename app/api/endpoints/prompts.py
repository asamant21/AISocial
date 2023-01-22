from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from datetime import datetime

prefix = """
You are provided a list of tweets that a particular Twitter user has liked in the past.

Use the guidelines below to create your own tweet.

The tweets are provided in the following JSON Format:
{{
    "tweet": the content of the tweet
    "user": the user name of the tweet publisher
}}.
"""
suffix = """
Guidelines for Creating Your Own Tweet:
- You should use a writing tone similar to those in the tweets above eg. funny, informative, etc. Don't limit yourself to these. Be specific.
- You should pretend to be each of the users described above. Take on their personality.
- You should write on some of the topics that are used in the tweets above, but don't limit yourself. Talk about new things!
- Never repeat information in the tweets above. Be original
- Don't mention dates in the past
- Be opinionated in what you say. Don't be afraid to say something controversial.


Tweet JSON Result Format:
{
    "tweet": "the tweet itself",
    "user": "the username that created the tweet. taken from the list of usernames above.",
    "tone": "the tone of the tweet that you wrote",
    "topic": :topics that you decided to write about"
}

Output:"""
eg_template = """{tweets}"""

day_quote = """
Today's date is: {today}
"""
eg_prompt = PromptTemplate(template=eg_template, input_variables=["tweets"])