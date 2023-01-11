"""Base Class for a Post."""
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Extra

from aisocial.Topic import topic_cache


class ContentType(str, Enum):
    """Post Type (used to identify different posts)"""

    TEXT = "Text"
    IMAGE = "Image"


class BasePost(BaseModel):
    """Base Topic is the base class for topics"""

    post_id: str  # post_id is unique identifier
    content: str
    topics: List[str] = []
    created_time: datetime
    is_shown: bool = False
    is_liked: bool = False
    metadata: dict = {}

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def show(self) -> None:
        """Show post."""
        if self.is_shown:
            return
        self.is_shown = True
        for topic_name in self.topics:
            curr_topic = topic_cache[topic_name]
            curr_topic.num_posts_shown += 1
            topic_cache[topic_name] = curr_topic

    def like(self):
        if self.is_liked:
            return
        self.is_liked = True
        for topic_name in self.topics:
            curr_topic = topic_cache[topic_name]
            curr_topic.num_posts_liked += 1
            curr_topic.update_rec_rating(1)
            topic_cache[topic_name] = curr_topic

    @abstractmethod
    def content_type(self) -> ContentType:
        """Returns Content Type."""


class TextPost(BasePost, BaseModel):
    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def content_type(self) -> ContentType:
        """Return Content Type."""
        return ContentType.TEXT
