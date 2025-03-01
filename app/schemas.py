from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from enum import Enum

class EventStatus(str, Enum):
    scheduled = "scheduled"
    ongoing = "ongoing"
    completed = "completed"
    canceled = "canceled"

class EventCreate(BaseModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int

class EventResponse(EventCreate):
    event_id: int
    status: EventStatus

    model_config = ConfigDict(from_attributes=True)  # ✅ Updated for Pydantic v2

class AttendeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

class AttendeeResponse(AttendeeCreate):
    attendee_id: int
    event_id: int
    check_in_status: bool

    model_config = ConfigDict(from_attributes=True)  # ✅ Updated for Pydantic v2
