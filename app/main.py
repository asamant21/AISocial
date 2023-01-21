""""""
import os

from flask import Flask
from flask_cors import CORS
from supabase import create_client, Client


app = Flask(__name__)
app.debug = True
CORS(app)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


@app.route('/generate-post')
def generate_post():
    user_id = get_user_id()
    # Returned data schema:
    # [{'id': 1,
    #   'created_at': '2023-01-21T22:09:53+00:00',
    #   'tweet_id': 1,
    #   'user_id': 1,
    #   'child_like_count': 1,
    #   'liked': True}]
    impressions = supabase.table("Impression").select("*").filter("user_id", "eq", user_id).execute().data
    pass


def get_user_id():
    return 1


@app.route('/like-tweet', methods=["POST"])
def like_tweet():
    pass

