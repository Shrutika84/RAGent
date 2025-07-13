from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.config import SessionLocal
from app.db import crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class EventCreate(BaseModel):
    user_id: str
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime

class EventOut(EventCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

@router.post("/create", response_model=EventOut)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db, event.dict())

@router.get("/list/{user_id}", response_model=List[EventOut])
def list_events(user_id: str, db: Session = Depends(get_db)):
    return crud.get_events_for_user(db, user_id)
