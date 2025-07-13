from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import crud, models
from app.config import SessionLocal
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(BaseModel):
    user_id: str
    name: str
    company: Optional[str] = None
    email: Optional[str] = None

class ConversationLogOut(BaseModel):
    role: str
    message: str
    timestamp: str
    topic: Optional[str] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True

@router.post("/create_user")
def create_user(user: User, db: Session = Depends(get_db)):
    return crud.create_user(db, user.dict())

@router.put("/update_user")
def update_user(user: User, db: Session = Depends(get_db)):
    return crud.update_user(db, user.user_id, user.dict())

@router.get("/conversations/{user_id}", response_model=List[ConversationLogOut])
def get_conversations(user_id: str, db: Session = Depends(get_db)):
    return crud.get_conversation_history(db, user_id)
