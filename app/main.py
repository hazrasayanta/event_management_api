from fastapi import FastAPI
from app.database import engine, Base
from app.routes import auth, events, attendees

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(attendees.router)
