"""Endpoints for generating tweets."""

from fastapi import APIRouter
from api import schemas

router = APIRouter()


@router.get("", response_model=schemas.Tweet)
def generate():
    """Generate a tweet for the user."""

    return {"id": 1, "content": "foo", "author": "foo"}
