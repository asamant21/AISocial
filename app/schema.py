from pydantic import BaseModel, Field, validator, EmailStr


class Tweet(BaseModel):
    """Base class for Tweet."""
    id: int
    content: str
    author: str
