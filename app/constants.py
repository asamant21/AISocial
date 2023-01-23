"""App constants."""

# Impression table schema:
# {'id': 1,
#   'created_at': '2023-01-21T22:09:53+00:00',
#   'tweet_id': 1,
#   'user_id': 1,
#   'child_like_count': 1,
#   'liked': True}
IMPRESSION_TABLE_NAME = "Impression"
IMPRESSION_TABLE_ID = "id"
IMPRESSION_TABLE_USER_ID = "user_uid"
IMPRESSION_TABLE_TWEET_ID = "tweet_id"
IMPRESSION_TABLE_CREATED_TIME = "created_at"
IMPRESSION_TABLE_LIKED = "liked"
IMPRESSION_TABLE_CHILD_LIKE_COUNT = "child_like_count"

# Tweet table schema:
# {'id': 6,
#   'created_at': '2023-01-21T22:54:52.770345+00:00',
#   'content': 'insert',
#   'author': 'test2',
#   'metadata': {'prompt_example_tweet_ids': [1, 2, 3]}}
TWEET_TABLE_NAME = "Tweet"
TWEET_TABLE_ID = "id"
TWEET_TABLE_AUTHOR = "author"
TWEET_TABLE_CONTENT = "content"
TWEET_TABLE_METADATA = "metadata"
TWEET_METADATA_PROMPT_TWEET_IDS = "prompt_example_tweet_ids"

SUPABASE_TRUE_VAL = "true"
SUPABASE_FALSE_VAL = "false"

SEED_TWEET_IDS = [7, 8, 9, 10, 11]
