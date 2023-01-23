"""Streamlit server file."""
from typing import Dict, List

import streamlit as st
from streamlit_tags import st_tags

import aisocial
from aisocial.main import generate_post
from aisocial.Post import BasePost, ImagePost, TextPost
from aisocial.Topic import (BaseTopic, add_user_recommended_topics,
                            generate_new_topics)

MAX_SEED_TOPICS_NUM = 50

if "topic_cache" not in st.session_state:
    st.session_state["topic_cache"]: Dict[str, BaseTopic] = {}


if "post_cache" not in st.session_state:
    st.session_state["post_cache"]: Dict[str, BasePost] = {}

if "post_list" not in st.session_state:
    st.session_state["post_list"]: List[BasePost] = []


def like_post(post_id: str) -> None:
    aisocial.Post.post_cache[post_id].like()


def generate_new_posts(num_posts: int = 3) -> List[BasePost]:
    posts: List[BasePost] = []
    for i in range(num_posts):
        post = generate_post()
        if post is None:
            continue
        posts.append(post)
    return posts


def like_and_generate(post_id: str) -> None:
    like_post(post_id)
    st.session_state["post_list"].extend(generate_new_posts(1))


def show_posts(posts: List[BasePost]) -> None:
    for curr_post in posts:
        curr_post.show()
        if isinstance(curr_post, TextPost):
            st.markdown(f"<div style=\"text-align: center;\">{curr_post.content}</div>", unsafe_allow_html=True)
            st.button(f"Like Post", key=curr_post.post_id, on_click=like_and_generate, args=[curr_post.post_id])
        else:
            st.image(curr_post.content)
            st.button(f"Like Post", key=curr_post.post_id, on_click=like_and_generate, args=[curr_post.post_id])


st.set_page_config(page_title="AI Social Media", page_icon=":robot:")
st.title("AI Social Media")
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
m = st.markdown(
    """
    <style>
        div.stButton > button:first-child {
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
        }
</style>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <style>
        [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)


def request_user_topics():
    input_topics = st_tags(
        maxtags=-1,
        text="Tell me about some things that you like",
        label="### Topics that you follow: ",
        key="input"
    )
    return input_topics


user_topics = request_user_topics()
show_posts(st.session_state["post_list"])

if len(user_topics):
    add_user_recommended_topics(user_topics)

    if len(aisocial.Topic.topic_cache) < MAX_SEED_TOPICS_NUM:
        generate_new_topics()

image_spinner_placeholder = st.empty()
post_list: List[BasePost] = []
placeholder = st.empty()
isclick = placeholder.button('Generate Recommendations')
if isclick:
    with image_spinner_placeholder:
        with st.spinner("Please wait while your posts are being generated..."):
            for i in range(3):
                post = generate_post()
                if post is None:
                    continue
                post_list.append(post)
    st.session_state["post_list"].extend(post_list)
    placeholder.empty()

show_posts(post_list)

# Always update caches
st.session_state["topic_cache"] = aisocial.Topic.topic_cache
st.session_state["post_cache"] = aisocial.Post.post_cache

