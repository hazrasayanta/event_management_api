import csv
from io import StringIO
from sqlalchemy.orm import Session
from app.models import Event, Attendee
from app.schemas import EventCreate, EventUpdate, AttendeeCreate
from datetime import datetime
from fastapi import HTTPException

# 1️. Create Event
def create_event(db: Session, event_data: EventCreate, organizer_id: int):
    new_event = Event(**event_data.dict(), status="scheduled", organizer_id=organizer_id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

# 2️. Get Events (with Filters)
def get_events(db: Session, status=None, location=None, date=None):
    query = db.query(Event)
    
    if status:
        query = query.filter(Event.status == status)
    if location:
        query = query.filter(Event.location == location)
    if date:
        query = query.filter(Event.start_time >= datetime.strptime(date, "%Y-%m-%d"))

    return query.all()

# 3️. Get Event by ID
def get_event_by_id(db: Session, event_id: int):
    return db.query(Event).filter(Event.event_id == event_id).first()

# 4️. Update Event
def update_event(db: Session, db_event: Event, event_update: EventUpdate):
    for key, value in event_update.dict(exclude_unset=True).items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

# 5️. Register Attendee
def register_attendee(db: Session, event_id: int, current_user):
    event = get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Check if event is already full
    if db.query(Attendee).filter(Attendee.event_id == event_id).count() >= event.max_attendees:
        raise HTTPException(status_code=400, detail="Event is full")

    # Fetch the existing attendee
    existing_attendee = db.query(Attendee).filter(
        Attendee.email == current_user.email
    ).first()
    
    if not existing_attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")

    # Check if already registered for the event
    if existing_attendee.event_id == event_id:
        raise HTTPException(status_code=400, detail="You are already registered for this event")

    # Associate the attendee with the event
    existing_attendee.event_id = event_id

    db.commit()
    db.refresh(existing_attendee)

    return {
        "id": existing_attendee.id,  # ✅ Added id field
        "first_name": existing_attendee.first_name,
        "last_name": existing_attendee.last_name,
        "email": existing_attendee.email,
        "event_id": existing_attendee.event_id,
        "check_in_status": existing_attendee.check_in_status
    }

# 6️. Check-in Attendee
def check_in_attendee(db: Session, event_id: int, current_user: Attendee):
    print(f"Checking in for event_id: {event_id}, user email: {current_user.email}")

    attendee = db.query(Attendee).filter(
        Attendee.email == current_user.email, Attendee.event_id == event_id
    ).first()

    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee not found for this event")

    if attendee.check_in_status:
        raise HTTPException(status_code=400, detail="Already checked in")

    attendee.check_in_status = True
    db.commit()
    db.refresh(attendee)
    return {"message": "Check-in successful"}

# 7️. Get Attendees (With Optional Check-in Filter)
def get_attendees(db: Session, event_id: int, check_in_status=None):
    query = db.query(Attendee).filter(Attendee.event_id == event_id)
    
    if check_in_status is not None:
        query = query.filter(Attendee.check_in_status == check_in_status)

    return query.all()

# 8️. Bulk Check-in Attendees (Only Organizers Can Bulk Check-in)
def bulk_check_in_attendees(db: Session, event_id: int, organizer_id: int, csv_content: str):
    # Verify if event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Ensure only the organizer can upload CSV
    if event.organizer_id != organizer_id:
        raise HTTPException(status_code=403, detail="Only the event organizer can upload check-in CSV")

    csv_reader = csv.DictReader(StringIO(csv_content))

    updated_attendees = []
    not_found_attendees = []

    for row in csv_reader:
        email = row.get("email")
        if not email:
            continue

        attendee = db.query(Attendee).filter(
            Attendee.email == email, Attendee.event_id == event_id
        ).first()

        if attendee:
            if not attendee.check_in_status:  # Avoid duplicate check-ins
                attendee.check_in_status = True
                updated_attendees.append(email)
        else:
            not_found_attendees.append(email)

    db.commit()

    return {
        "checked_in": updated_attendees,
        "not_found": not_found_attendees
    }
