from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database

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
