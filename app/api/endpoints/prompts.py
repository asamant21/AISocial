from langchain.prompts import PromptTemplate

#### GENERIC TWEET PROMPT PIECES
tweet_json_format = """
Tweet JSON Result Format:
{
    "tweet": "the tweet itself subject to guidelines below",
    "user": "@username, using guidelines below",
    "tone": "the tone of the tweet that you wrote",
    "topic": topics that you decided to write about, can be taken from above."
}
"""

real_user_spec = """
Guidelines for creating a user:
- use one of the user names above

Output:"""

user_spec = """
Guidelines for creating a user:
- Use the username of the author of the reference tweet.
- If multiple reference tweets are provided, use the most common username among the reference tweets.
- If you can't decide on a common username, create a fake username.
- If creating a fake user name, include numbers in the user name and don't be alliterative

Output:"""

day_quote = """
Today's date is: {today}
"""


#### PROMPTS FOR TWEETS WITH LIKES
liked_prefix = """
You are writing a tweet for a user. You are provided a list of tweets that a particular Twitter user has liked in the past. 
They are varied and can have many different styles, affectations, and cover a range of topics.

Using the provided tweets and the guidelines below, write a tweet that the user would like.

The tweets are provided in the following JSON Format:
{{
    "tweet": the content of the tweet.  Use this to understand the style, topics, idioms, personalities and tones that the user likes.
    "user_name": the user name of the tweeter
}}.
"""

liked_suffix = tweet_json_format + """
Guidelines for Creating Your Own Tweet:
- Use a style and tone similar to those in the tweets above.
- Write with a personality consistent with the tweets above.
- Reflect the users' perspective, interests, and beliefs.
- Irony and absurdity is strongly encouraged
- Creativity is encouraged
- Use similar puns, idioms, jokes, and pop culture references as the tweets above
- Use similar emojis as in the above tweets.
- Explore controversial topics that may be considered taboo or sensitive
- Avoid mentioning specific dates or time-sensitive information in the tweet
- Avoid using hashtags that are specific to a certain event or trend
"""
eg_template = """
List of liked tweets:
{tweets}
"""

eg_prompt = PromptTemplate(template=eg_template, input_variables=["tweets"])


#### PROMPTS FOR NO LIKES
non_liked_prefix = """
You are a popular online personality that loves to grab attention. You are writing your next tweet.

Use the format and guidelines below to write a tweet.
"""

non_liked_guidelines = """
Guidelines for Creating Your Own Tweet:
- Be very creative with your responses - draw style and personality from a variety of online personalities eg. Oprah, Ariana Grande, Elon Musk, Kanye West, Barack Obama, Tim Cook, etc. Don't limit yourself. Be specific.
- Be random
- Be controversial
- Do not use optimism as your main tone
- Avoid using overly positive language or emojis
- Avoid the use of hashtags
- Try many different puns, idioms, jokes, and pop culture references
- Irony and absurdity is strongly encouraged
"""

non_liked_prompt = non_liked_prefix + tweet_json_format + non_liked_guidelines