import json
import os
from typing import List, Type, Union

from flask import Flask, abort, request
from flask_cors import CORS
from flask import jsonify
import numpy as np
from supabase import create_client, Client


app = Flask(__name__)
app.debug = True
CORS(app)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


@app.route('/generate-post  ')
def generate_post():
    pass


@app.route('/like-tweet', methods=["POST"])
def like_tweet():
    pass
