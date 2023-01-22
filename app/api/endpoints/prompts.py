from langchain.prompts import FewShotPromptTemplate, PromptTemplate

prefix = """
You are writing a tweet for a user. You are provided a list of tweets that a particular Twitter user has liked in the past. 
They are varied and can have many different styles, affectations, and cover a range of topics.

Using the provided tweets and the guidelines below, write a tweet that the user would like.

The tweets are provided in the following JSON Format:
{{
    "tweet": the content of the tweet.  Use this to understand the style, topics, idioms, personalities and tones that the user likes.
    "user": the user name of the tweeter
}}.
"""
suffix = """
Tweet JSON Result Format:
{
    "tweet": "the tweet itself subject to guidelines below",
    "user": "@username, using guidelines below",
    "tone": "the tone of the tweet that you wrote",
    "topic": topics that you decided to write about, can be taken from above."
}

Guidelines for Creating Your Own Tweet:
- Use a style and tone similar to those in the tweets above.
- Write with a personality consistent with the tweets above.
- Reflect the users' perspective, interests, and beliefs.
- Use similar puns, idioms, jokes, and pop culture references as the tweets above.
- Use similar hashtags and emojis as in the above tweets.
- Explore controversial topics that may be considered taboo or sensitive
- If mentioning a date, don't use a past one
- Irony and absurdity is encouraged
- Creativity is encouraged

Guidelines for creating a user:
- either use one of the user names above OR create a fake one according the the rules below.

Rules for creating a fake user:
- include numbers in the user name, don't be always be alliterative
- user names do not have to releate to the personality or style decided
- Be creative and expressive 


Output:"""
eg_template = """
List of liked tweets:
{tweets}
"""

day_quote = """
Today's date is: {today}
"""
eg_prompt = PromptTemplate(template=eg_template, input_variables=["tweets"])