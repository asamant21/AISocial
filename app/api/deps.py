"""Dependencies for endpoints."""

from datetime import datetime, timezone

from dateutil import parser
from fastapi import Header, HTTPException, status
from gotrue import UserAttributes
from gotrue.helpers import parse_user_response

from app.config import key, url
from supabase import Client, create_client


def get_current_user(authorization: str = Header(None)) -> str:
    """User either a jwt token or api key to get the current user."""
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
            return str(supabase_user.id)
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


def get_regen_time(authorization: str = Header(None)) -> datetime:
    """Get the last regeneration time of a user to query."""
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
            user_metadata = supabase_user.user_metadata
            if "regeneration_time" in user_metadata:
                try:
                    return parser.parse(user_metadata["regeneration_time"])
                except:
                    pass
            return datetime.min
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


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
