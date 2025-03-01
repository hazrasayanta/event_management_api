from sqlalchemy.orm import Session
from app.models import Event, Attendee
from app.schemas import EventCreate, AttendeeCreate

def create_event(db: Session, event: EventCreate):
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session):
    return db.query(Event).all()

def create_attendee(db: Session, event_id: int, attendee: AttendeeCreate):
    db_attendee = Attendee(**attendee.dict(), event_id=event_id)
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)
    return db_attendee
