from pydantic import BaseModel
from datetime import date, time

class EventCreate(BaseModel):
    title: str
    description: str
    date: date
    time: time
    venue: str

class Event(BaseModel):
    id: int
    title: str
    description: str
    date: date
    time: time
    venue: str

    class Config:
        from_attributes = True

class RegistrationCreate(BaseModel):
    event_id: int
    name: str
    email: str

class Registration(BaseModel):
    id: int
    event_id: int
    name: str
    email: str

    class Config:
        from_attributes = True
