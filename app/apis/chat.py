from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict
from sqlalchemy.orm import Session
from datetime import datetime

from app.llm import get_chat_response
from app.rag import retrieve_relevant_chunks
from app.db import crud
from app.config import SessionLocal
import time
router = APIRouter()

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def infer_tags(message: str):
    if "rent" in message.lower():
        return "Pricing", "Inquiring"
    elif "lease" in message.lower():
        return "Leasing", "Inquiring"
    elif "available" in message.lower():
        return "Availability", "Inquiring"
    elif "thank" in message.lower() or "great" in message.lower():
        return "General", "Resolved"
    else:
        return "General", "Unresolved"

class ChatRequest(BaseModel):
    user_id: str
    message: str
    history: List[Dict] = []

@router.post("/")
async def chat_with_user(payload: ChatRequest, db: Session = Depends(get_db)):
    start_time = time.time()  # Start timer
    rag_context = retrieve_relevant_chunks(payload.message)

    reply = get_chat_response(
        user_message=payload.message,
        rag_context=rag_context,
        history=payload.history
    )

    topic, status = infer_tags(payload.message)

    crud.log_message(db, payload.user_id, role="user", message=payload.message, topic=topic, status=status)
    crud.log_message(db, payload.user_id, role="assistant", message=reply, topic=topic, status="Resolved")

    # Calendar integration
    events = crud.get_events_for_user(db, payload.user_id)
    upcoming = [e for e in events if e.start_time > datetime.utcnow()]
    event_list = "\n".join(
        [f"- {e.title} at {e.start_time.strftime('%Y-%m-%d %H:%M')}" for e in upcoming[:3]]
    )
    reply_with_events = reply + (f"\n\n Upcoming Events:\n{event_list}" if upcoming else "")
    duration = round(time.time() - start_time, 2)  # ⏱️ Add this line

    return {
        "user_id": payload.user_id,
        "message": payload.message,
        "rag_context": rag_context,
        "response": reply_with_events,
        "response_time": f"{duration} seconds"
    }
