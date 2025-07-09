from sqlalchemy import Column, Integer, String, Text, Date, Time, ForeignKey
from .database import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(Text)
    date = Column(Date)
    time = Column(Time)
    venue = Column(String(100))

class Registration(Base):
    __tablename__ = "registrations"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    name = Column(String(100))
    email = Column(String(100))
