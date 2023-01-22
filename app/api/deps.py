"""Dependencies for endpoints."""

from fastapi import HTTPException, status, Header

from app.config import supabase as client




def get_current_user(
        authorization: str = Header(None)
) -> str:
    """User either a jwt token or api key to get the current user."""
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )
    id_token = authorization.replace("Bearer ", "")
    try:
        supabase_user = client.auth.api.get_user(jwt=id_token)
        if supabase_user is not None:
            return str(supabase_user.id)
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

