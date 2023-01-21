import json

from flask import Flask, abort, request
from flask_cors import CORS
from typing import List, Type, Union
from flask import jsonify
import numpy as np

app = Flask(__name__)
app.debug = True
CORS(app)

import json
with open('../langchain/notebooks/tweets.json', 'r') as f:
    tweets_config = json.load(f)

import pandas as pd
df = pd.DataFrame(tweets_config)

df['weight'] = 1

from langchain.prompts.example_selector.base import BaseExampleSelector

from typing import Any, Dict, List
from langchain.prompts.example_selector.base import BaseExampleSelector
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
llm = OpenAI()
from langchain.chains import LLMChain

import contextlib
CONTEXT = {}
ID_TO_INDS = {}
GLOBAL_INFO = {}

@contextlib.contextmanager
def set_context(**kwargs):
    global CONTEXT
    CONTEXT = kwargs
    yield
    CONTEXT = {}

    
class CustomExampleSelector(BaseExampleSelector):
    """Interface for selecting examples to include in prompts."""
    
    def __init__(self, df):
        self.df = df

    def add_example(self, example: Dict[str, str]) -> Any:
        """Add new example to store for a key."""
        example['weight'] = 100
        self.df = self.df.append(example, ignore_index = True)

    def select_examples(self, input_variables: Dict[str, str]) -> List[dict]:
        """Select which examples to use based on the inputs."""
        global CONTEXT
        indices = np.random.choice(list(range(df.shape[0])), size=5, p=df['weight']/sum(df['weight']))
        ID_TO_INDS[CONTEXT["id"]] = indices
        return df.iloc[indices][['tweet', 'user']].to_dict(orient='records')

prefix = "This is the like history of a particular user on Twitter. All the likes have something in common."
suffix = """"content":"""
eg_template = """"content": {tweet}
"user": {user}
"""
eg_prompt = PromptTemplate(template=eg_template, input_variables=["user", "tweet"])
from langchain.prompts import FewShotPromptTemplate
eg_selector = CustomExampleSelector(df)
prompt_temp = FewShotPromptTemplate(prefix=prefix, suffix=suffix, example_prompt=eg_prompt, example_selector=eg_selector, input_variables=[])

@app.route('/generate')
def generate():
    global GLOBAL_INFO
    _id = "1"
    with set_context(id=_id):
        gen_tweet = llm(prompt_temp.format())
    tweet, user = gen_tweet.strip().split('\n"user": ')
    GLOBAL_INFO["tweet"] = tweet
    GLOBAL_INFO["user"] = user
    return jsonify({"tweet": tweet, "user": user, "id": "_id"})

# Endpoint to create a new guide
@app.route('/feedback', methods=["POST"])
def feedback():
    global CONTEXT
    global GLOBAL_INFO
    for i in ID_TO_INDS["1"]:
        print(i)
        eg_selector.df.loc[i, "weight"] = eg_selector.df.iloc[i]["weight"] + 1
    eg_selector.add_example({"tweet": GLOBAL_INFO["tweet"], "user": GLOBAL_INFO["user"]})
    print(eg_selector.df)
    return jsonify({})
