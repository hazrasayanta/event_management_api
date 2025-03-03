from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# User Model (For Organizers Only)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # Only Organizers Need Authentication
    role = Column(String, default="organizer")  # Role-based access ("organizer" or "attendee")

    events = relationship("Event", back_populates="organizer")


# Event Model
class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    max_attendees = Column(Integer, nullable=False)
    status = Column(String, default="scheduled")
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    organizer = relationship("User", back_populates="events")
    attendees = relationship("Attendee", back_populates="event")


# Attendee Model (Fixed)
class Attendee(Base):
    __tablename__ = "attendees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    event_id = Column(Integer, ForeignKey("events.event_id"), nullable=True)
    check_in_status = Column(Boolean, default=False)

    event = relationship("Event", back_populates="attendees")
