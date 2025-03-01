from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Attendee
from app.schemas import EventCreate, EventResponse
from app.crud import create_event, get_events
from app.routes.auth import get_current_user

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/", response_model=EventResponse)
def create_new_event(event: EventCreate, db: Session = Depends(get_db), current_user: Attendee = Depends(get_current_user)):
    return create_event(db, event)

@router.get("/", response_model=list[EventResponse])
def list_all_events(db: Session = Depends(get_db)):
    return get_events(db)


