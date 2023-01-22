"""Endpoints for Tracer Sessions."""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.api import deps
from app import schema

router = APIRouter()


@router.get("/{session_id}", response_model=schema.TracerSession)
def read_tracer_session(session_id: int, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_active_user)):
    """Get a specific session."""
    db_tracer_session = crud.get_tracer_session(db, session_id)
    if db_tracer_session is None:
        raise HTTPException(status_code=404, detail="Tracer session not found")
    if db_tracer_session.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to view this tracer session")
    return db_tracer_session


@router.get("/generate", response_model=schema.Tweet)
def read_tracer_sessions(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user)
):
    """Get all sessions."""
    return crud.get_tracer_sessions_with_owner(db, current_user.id, skip, limit)


@router.post("/like/{tweet_id}")
def create_tracer_session(tracer_session: schemas.TracerSessionCreate, db: Session = Depends(deps.get_db), current_user: models.User = Depends(deps.get_current_active_user)):
    """Create a new session."""
    return crud.create_tracer_session_with_owner(db, tracer_session, current_user.id)