from pydantic import BaseModel
from datetime import date, time

class EventCreate(BaseModel):
    title: str
    description: str
    date: date
    time: time
    venue: str

class RegistrationCreate(BaseModel):
    event_id: int
    name: str
    email: str
