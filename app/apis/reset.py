from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from app.db import models
from app.config import SessionLocal

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request schema
class ResetRequest(BaseModel):
    user_id: Optional[str] = None

@router.post("/reset")
def reset_memory(data: ResetRequest, db: Session = Depends(get_db)):
    if data.user_id:
        deleted = db.query(models.ConversationLog).filter(
            models.ConversationLog.user_id == data.user_id
        ).delete()
        db.commit()
        return {"message": f"Cleared {deleted} messages for user {data.user_id}"}
    else:
        deleted = db.query(models.ConversationLog).delete()
        db.commit()
        return {"message": f"Cleared ALL user conversation history ({deleted} entries)"}
