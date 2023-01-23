from pydantic import BaseModel


class Tweet(BaseModel):
    id: int
    content: str
    author: str
    likes: int


class UserTweetView(Tweet):
    liked: bool
