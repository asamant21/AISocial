"""Dependencies for endpoints."""

from typing import Generator
from app.database import SessionLocal
from fastapi import Depends, HTTPException, status, Header
from app import models, schemas, crud
from sqlalchemy.orm import Session
from app.config import settings
import supabase



def get_db() -> Generator:
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), authorization: str = Header(None)
) -> models.User:
    """User either a jwt token or api key to get the current user."""
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )
    id_token = authorization.replace("Bearer ", "")
    try:
        client = supabase.create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        supabase_user = client.auth.api.get_user(jwt=id_token)
        if supabase_user is not None:
            user = crud.get_user_by_email(db, supabase_user.email)
            if user is None:
                user = crud.create_user(db, schemas.UserCreate(email=supabase_user.email))
            return user
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


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
