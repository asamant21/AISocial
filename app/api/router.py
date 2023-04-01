"""Initialize routers."""

from fastapi import APIRouter

from app.api.endpoints import generate, like, regenerate, retrieve_likes, retrieve_tweet, update_number

api_router = APIRouter()
api_router.include_router(generate.router, prefix="/generate", tags=["generate"])
api_router.include_router(regenerate.router, prefix="/regenerate", tags=["regenerate"])
api_router.include_router(like.router, prefix="/like", tags=["like"])
api_router.include_router(
    retrieve_tweet.router, prefix="/retrieve-tweet", tags=["retrieve tweet"]
)
api_router.include_router(
    retrieve_likes.router, prefix="/retrieve-likes", tags=["retrieve liked tweets"]
)
api_router.include_router(
    update_number.router, prefix="/update-number", tags=["update a user's phone number"]
)

