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

SUMMARY_TABLE_NAME = "Summaries"
SUMMARY_TABLE_NUM = "user_num"
SUMMARY_TABLE_LINK = "link"
SUMMARY_TABLE_MAIN_SUMMARY = "summary"
SUMMARY_TABLE_PERSONA = "persona"
SUMMARY_TABLE_SYNTHESIS = "synthesis"

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
TWEET_METADATA_ORIGIN_USER_NUM = "origin_user_num"
TWEET_METADATA_ORIGIN_USER_NAME = "origin_user_name"

FRIEND_TABLE_NAME = "Friends"
FRIEND_TABLE_USER_NUM = "user_num"
FRIEND_TABLE_FRIEND_NUM = "friend_num"
FRIEND_TABLE_ACCEPTED = "accepted"

SUPABASE_TRUE_VAL = "true"
SUPABASE_FALSE_VAL = "false"

SEED_TWEET_IDS = [
    260,
    261,
    262,
    263,
    264,
    265,
    266,
    267,
    268,
    269,
    270,
    271,
    272,
    273,
    274,
    275,
    276,
    277,
    278,
    279,
    280,
    281,
    282,
    283,
    284,
    285,
    286,
    287,
    288,
    289,
    290,
    291,
    292,
    293,
    294,
    295,
    296,
    297,
    298,
    299,
    300,
    301,
    302,
    303,
    304,
    305,
    306,
    307,
    308,
    309,
    310,
    311,
    312,
    313,
    314,
    315,
    316,
    317,
    318,
    319,
    320,
    321,
    322,
    323,
    324,
    325,
    326,
    327,
    328,
    329,
    330,
    331,
    332,
    333,
    334,
    335,
    336,
    337,
    338,
    339,
    340,
    341,
    342,
    343,
    344,
    345,
    346,
    347,
    348,
    349,
    955,
    956,
    957,
    958,
    959,
    960,
    961,
    962,
    963,
    964,
    965,
    966,
    967,
    968,
    969,
    970,
    971,
    972,
    973,
    974,
]
