from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from enum import Enum
from typing import Optional

# Event Status Enum
class EventStatus(str, Enum):
    scheduled = "scheduled"
    ongoing = "ongoing"
    completed = "completed"
    canceled = "canceled"

# Event Creation Schema
class EventCreate(BaseModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int

# Event Response Schema
class EventResponse(EventCreate):
    event_id: int
    status: EventStatus

    model_config = ConfigDict(from_attributes=True)  # Updated for Pydantic v2

# New: Event Update Schema
class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    max_attendees: Optional[int] = None
    status: Optional[EventStatus] = None

# Attendee Creation Schema (Fixed: Added Password)
class AttendeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str  
    phone_number: Optional[str] = None

# Attendee Response Schema
class AttendeeResponse(BaseModel):
    id: int
    event_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    check_in_status: bool

    model_config = ConfigDict(from_attributes=True)  # Updated for Pydantic v2
