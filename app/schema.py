""""""
from pydantic import BaseModel


class Tweet(BaseModel):
    """Base class for Tweet."""
    id: int
    content: str
    author: str
