"""Streamlit server file."""
import streamlit as st
import aisocial
from typing import Dict, List
from streamlit_tags import st_tags
from aisocial.main import generate_post
from aisocial.Post import BasePost, TextPost, ImagePost
from aisocial.Topic import BaseTopic, generate_new_topics, add_user_recommended_topics

MAX_SEED_TOPICS_NUM = 50

if "topic_cache" not in st.session_state:
    st.session_state["topic_cache"]: Dict[str, BaseTopic] = {}


if "post_cache" not in st.session_state:
    st.session_state["post_cache"]: Dict[str, BasePost] = {}


def like_post(post_id: str) -> None:
    aisocial.Post.post_cache[post_id].like()


st.set_page_config(page_title="AI Social Media", page_icon=":robot:")
st.write(
    """<style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>""",
    unsafe_allow_html=True,
)


def request_user_topics():
    input_topics = st_tags(
        maxtags=-1,
        text="Tell me about some things that you like: ",
        key="input"
    )
    return input_topics


user_topics = request_user_topics()
print(f"Post Cache: {aisocial.Post.post_cache}")

if len(user_topics):
    add_user_recommended_topics(user_topics)
    st.session_state["topic_cache"] = aisocial.Topic.topic_cache

while len(aisocial.Topic.topic_cache) < MAX_SEED_TOPICS_NUM:
    generate_new_topics()

if st.button('Generate Recommendations'):
    post_list: List[BasePost] = []
    for i in range(3):
        post = generate_post()
        post.show()
        post_list.append(post)

    for i in range(3):
        curr_post = post_list[i]

        if isinstance(curr_post, TextPost):
            st.write(curr_post.content)
        else:
            st.image(curr_post.content, use_column_width=True)

        st.button(f"Like Post", key=curr_post.post_id, on_click=like_post, args=[curr_post.post_id])

    st.session_state["post_cache"] = aisocial.Post.post_cache
