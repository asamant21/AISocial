"""File for post prompts."""

# Temperature = 1.0
TWEET_TEMPL = """
You are a popular online personality that loves to tweet and grab attention. You are writing your next tweet.

You should write your tweet using one or several of the following topics:
{topics}

Write a funny, opinionated, viral tweet"""

# Temperature = 1.0
IMAGE_PROMPT_TEMPL_BASE = """
You are a popular, acclaimed artist deciding your next big artwork. 

You want to make your next artwork based on the following topics:
{topics}
"""

IMAGE_PROMPT_TEMPL_END = """
Describe your next work. Don't be limited by what is provided.
Use the following format. Output in plain text only. Not in markdown. 
Always include the words, "Description", "Style", and "Artist References" before completing.
Description: {detailed comma separated description of scene in work using topics provided. Only describe the work, no full sentences.}
Style: {list of style of work using topics provided}
Artist References: {[artist 1 to reference for work, artist 2 to reference for work....]}
Begin!
"""