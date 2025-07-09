from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend import models, schemas, database
from fastapi import Path, Query

# Create tables if not exist
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Allow all origins (for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is working!"}

@app.post("/events")
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    return {"message": "Event created!"}

@app.get("/events")
def get_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()

@app.post("/register")
def register(registration: schemas.RegistrationCreate, db: Session = Depends(get_db)):
    new_registration = models.Registration(**registration.dict())
    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)
    return {"message": "Registered successfully"}



@app.get("/create-sample")
def create_sample(db: Session = Depends(get_db)):
    e1 = models.Event(
        title="Tech Talk",
        description="A seminar about latest tech trends",
        date="2025-07-20",
        time="10:00:00",
        venue="Auditorium"
    )
    e2 = models.Event(
        title="Coding Contest",
        description="A 2-hour coding competition",
        date="2025-07-22",
        time="14:00:00",
        venue="Lab 2"
    )
    db.add_all([e1, e2])
    db.commit()
    return {"message": "Sample events added"}

@app.put("/events/{event_id}")
def update_event(
    event_id: int = Path(..., description="ID of the event to update"),
    event: schemas.EventCreate = ...,
    db: Session = Depends(get_db)
):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    for key, value in event.dict().items():
        setattr(db_event, key, value)

    db.commit()
    db.refresh(db_event)
    return {"message": "Event updated successfully!", "event": db_event}

@app.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted successfully!"}

@app.get("/events/{event_id}/registrations", response_model=List[schemas.Registration])
def get_event_registrations(event_id: int, db: Session = Depends(get_db)):
    registrations = db.query(models.Registration).filter(
        models.Registration.event_id == event_id
    ).all()
    return registrations

@app.get("/events/search", response_model=List[schemas.Event])
def search_events(name: str = Query(..., description="Name to search"), db: Session = Depends(get_db)):
    results = db.query(models.Event).filter(models.Event.title.ilike(f"%{name}%")).all()
    return results

@app.post("/registrations", response_model=schemas.Registration)
def create_registration(registration: schemas.RegistrationCreate, db: Session = Depends(get_db)):
    db_registration = models.Registration(**registration.dict())
    db.add(db_registration)
    db.commit()
    db.refresh(db_registration)
    return db_registration
