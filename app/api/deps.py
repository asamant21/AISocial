"""Dependencies for endpoints."""

from datetime import datetime, timezone

from dateutil import parser
from fastapi import Header, HTTPException, status
from gotrue import UserAttributes

from app.config import supabase as client


def get_current_user(authorization: str = Header(None)) -> str:
    """User either a jwt token or api key to get the current user."""
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )
    id_token = authorization.replace("Bearer ", "")
    try:
        supabase_user = client.auth.api.get_user(jwt=id_token)
        print(id_token)
        if supabase_user is not None:
            return str(supabase_user.id)
        else:
            print("None found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except Exception as e:
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
    try:
        supabase_user = client.auth.api.get_user(jwt=id_token)
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
    try:
        new_regen_time = datetime.now(timezone.utc)
        user_update = UserAttributes(
            data={"regeneration_time": new_regen_time.isoformat()}
        )
        supabase_user = client.auth.api.update_user(
            jwt=id_token, attributes=user_update
        )
        if supabase_user is not None:
            return new_regen_time
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
