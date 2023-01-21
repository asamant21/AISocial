from pydantic import BaseModel

class Tweet(BaseModel):
    id: int
    content: str
    author: str
