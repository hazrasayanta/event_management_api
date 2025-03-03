import csv
from io import StringIO
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Event, User, Attendee
from app.schemas import EventCreate, EventResponse, EventUpdate, AttendeeCreate, AttendeeResponse
from app.crud import (
    bulk_check_in_attendees, create_event, get_events, get_event_by_id, update_event, 
    register_attendee, check_in_attendee, get_attendees
)
from app.routes.auth import get_current_user
from typing import List, Optional

router = APIRouter(prefix="/events", tags=["Events"])

# 1️. Create Event (Only Organizers Can Create Events)
@router.post("/", response_model=EventResponse)
def create_new_event(
    event: EventCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "organizer":
        raise HTTPException(status_code=403, detail="Only organizers can create events")
    
    return create_event(db, event, current_user.id)

# 2️. Update Event (Only Event Organizer Can Update)
@router.put("/{event_id}", response_model=EventResponse)
def update_event_details(
    event_id: int,
    event_update: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_event = get_event_by_id(db, event_id)
    
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    if db_event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this event")

    return update_event(db, db_event, event_update)

# 3️. Register Attendee (Anyone Can Register)
@router.post("/{event_id}/register", response_model=AttendeeResponse)
def register_for_event(
    event_id: int, 
    db: Session = Depends(get_db),
    current_user: Attendee = Depends(get_current_user)
):
    return register_attendee(db, event_id, current_user)

# 4️. Check-in Attendee (Only Registered Attendees Can Check-in)
@router.post("/{event_id}/check-in")
def check_in(
    event_id: int, 
    db: Session = Depends(get_db), 
    current_user: Attendee = Depends(get_current_user)
):
    return check_in_attendee(db, event_id, current_user)

# 5️. List Events (With Filters)
@router.get("/", response_model=List[EventResponse])
def list_all_events(
    db: Session = Depends(get_db),
    status: Optional[str] = None,
    location: Optional[str] = None,
    date: Optional[str] = None
):
    return get_events(db, status=status, location=location, date=date)

# 6️. List Attendees (With Filters)
@router.get("/{event_id}/attendees", response_model=List[AttendeeResponse])
def list_event_attendees(
    event_id: int, 
    db: Session = Depends(get_db),
    check_in_status: Optional[bool] = None
):
    return get_attendees(db, event_id, check_in_status)



# 7️. Bulk Check-in Attendees (Only Organizers Can Bulk Check-in)
@router.post("/{event_id}/bulk-check-in")
async def bulk_check_in(
    event_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Ensure user is authenticated
):
    # Validate CSV file format
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    # Read file content
    content = await file.read()
    decoded_content = content.decode("utf-8")

    return bulk_check_in_attendees(db, event_id, current_user.id, decoded_content)
