from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Dict
from sqlalchemy.orm import Session
from datetime import datetime

from app.llm import get_chat_response
from app.rag import retrieve_relevant_chunks
from app.db import crud
from app.config import SessionLocal

router = APIRouter()

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Tag inference
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

# Request model
class ChatRequest(BaseModel):
    user_id: str
    message: str
    history: List[Dict] = []

@router.post("/")
async def chat_with_agent(req: ChatRequest, db: Session = Depends(get_db)):
    # 1. Extract message and prior history
    user_message = req.message
    user_id = req.user_id
    prior_history = req.history

    # 2. Retrieve RAG context
    rag_chunks = retrieve_relevant_chunks(user_message)
    rag_context = "\n".join(rag_chunks)

    # 3. Combine prompt with RAG and history
    chat_prompt = f"User: {user_message}\n\nKnowledge Base:\n{rag_context}\n\nConversation History:\n{prior_history}"

    # 4. Generate response from LLM
    response = get_chat_response(chat_prompt)

    # 5. Auto-tag conversation
    topic, status = infer_tags(user_message)

    # 6. Save message and response to DB
    crud.save_conversation(
        db=db,
        user_id=user_id,
        user_message=user_message,
        bot_response=response,
        topic=topic,
        status=status,
        timestamp=datetime.utcnow()
    )

    return {
        "user_id": user_id,
        "response": response,
        "topic": topic,
        "status": status,
        "knowledge_used": rag_chunks
    }
