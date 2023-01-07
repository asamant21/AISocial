"""Base Class for a Topic."""
from typing import Any

from pydantic import BaseModel, Extra


class BaseTopic(BaseModel):
    """Base Topic is the base class for topics"""

    name: str  # Name of topic is unique identifier
    user_provided: bool = False
    num_posts_liked: int = 0
    num_posts_shown: int = 0
    recommendation_rating: float = 0
    metadata: dict = {}

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def update_post_feedback(self, was_liked: bool):
        if was_liked:
            self.num_posts_liked += 1
        self.num_posts_shown += 1

    def add_key_to_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value

    def update_rec_rating(self, adjustment: float):
        self.recommendation_rating += adjustment
