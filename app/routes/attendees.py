from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AttendeeCreate, AttendeeResponse
from app.crud import create_attendee

router = APIRouter(prefix="/attendees", tags=["Attendees"])

@router.post("/{event_id}", response_model=AttendeeResponse)
def register_attendee(event_id: int, attendee: AttendeeCreate, db: Session = Depends(get_db)):
    return create_attendee(db, event_id, attendee)
