"""Dependencies for endpoints."""

from datetime import datetime, timezone

from dateutil import parser
from fastapi import Header, HTTPException, status
from gotrue import UserAttributes
from gotrue.helpers import parse_user_response
from gotrue.types import User

from app.config import key, url
from supabase import Client, create_client


def get_current_user(authorization: str = Header(None)) -> User:
    """Use either a jwt token or api key to get the current user."""
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )
    id_token = authorization.replace("Bearer ", "")
    print(id_token)
    supabase: Client = create_client(url, key)
    try:
        supabase_user = supabase.auth.get_user(jwt=id_token).user
        if supabase_user is not None:
            return supabase_user
        else:
            print("Supabase User is None, but no primary error thrown")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except Exception as e:
        print(f"Generic Authorization Error Thrown: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def get_current_user_id(authorization: str = Header(None)) -> str:
    """Use either a jwt token or api key to get the current user id."""
    user = get_current_user(authorization)
    return str(user.id)
def get_current_user_jwt(authorization: str = Header(None)) -> str:
    """Return jwt token for current user."""
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )
    id_token = authorization.replace("Bearer ", "")
    supabase: Client = create_client(url, key)
    try:
        supabase_user = supabase.auth.get_user(jwt=id_token).user
        if supabase_user is not None:
            return id_token
        else:
            print("None found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except Exception as e:
        print(e)
        print("Some other error")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def update_user_phone_number(id_token: str, number: str) -> None:
    """Update phone number for current use."""
    supabase: Client = create_client(url, key)
    try:
        user_update = UserAttributes(
            phone=number
        )
        update_response = supabase.auth._request(
            "PUT",
            "user",
            body=user_update,
            jwt=id_token,
            xform=parse_user_response,
        )
        if update_response is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def get_regen_time(authorization: str = Header(None)) -> datetime:
    """Get the last regeneration time of a user to query."""
    supabase_user = get_current_user(authorization)
    user_metadata = supabase_user.user_metadata
    if "regeneration_time" in user_metadata:
        try:
            return parser.parse(user_metadata["regeneration_time"])
        except:
            pass
    return datetime.min


def update_regen_time(authorization: str = Header(None)) -> datetime:
    """Update the regeneration time of a user and return the time."""
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )
    id_token = authorization.replace("Bearer ", "")
    supabase: Client = create_client(url, key)
    try:
        new_regen_time = datetime.now(timezone.utc)
        user_update = UserAttributes(
            data={"regeneration_time": new_regen_time.isoformat()}
        )
        update_response = supabase.auth._request(
            "PUT",
            "user",
            body=user_update,
            jwt=id_token,
            xform=parse_user_response,
        )
        if update_response is not None:
            return new_regen_time
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
