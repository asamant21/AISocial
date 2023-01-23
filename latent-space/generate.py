from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

llm = OpenAI()

twitter_topics = llm("Write a list of 20 most popular non-political twitter topics:")

topics = [t.split('. ')[-1] for t in twitter_topics.split("\n")[2:]] + ["Politics"]

twitter_user_names = llm("Write a list of 10 made up twitter user names")

twitter_user_names1 = llm("Write a list of 10 real twitter user names")

users = [t.split('. ')[-1] for t in twitter_user_names.split("\n")[2:]] + [t.split('. ')[-1] for t in twitter_user_names1.split("\n")[2:]]

template = """The following is a tweet from {user} about {topic}:

"user": "{user}",
"topic": "{topic}",
"content":"""
prompt = PromptTemplate(template=template, input_variables=["user", "topic"])

import random

chain = LLMChain(llm=llm, prompt=prompt)

tweets_config = []
for _ in range(50):
    i = random.randint(0,19)
    j = random.randint(0,19)
    tweets_config.append({"user": users[i], "topic": topics[j]})


tweets = chain.apply(tweets_config)
for i in range(len(tweets_config)):
    tweets_config[i]['tweet'] = tweets[i]['text']

import json

with open('tweets.json', 'w') as f:
    json.dump(tweets_config, f)

