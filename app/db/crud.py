from sqlalchemy.orm import Session
from app.db import models
from datetime import datetime

def create_user(db: Session, user_data: dict):
    user = models.User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user_id: str, update_data: dict):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    return user

def log_message(db: Session, user_id: str, role: str, message: str, topic=None, status=None):
    log = models.ConversationLog(
        user_id=user_id,
        role=role,
        message=message,
        topic=topic,
        status=status,
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    return log

def get_conversation_history(db: Session, user_id: str, limit: int = 10):
    return db.query(models.ConversationLog)\
             .filter(models.ConversationLog.user_id == user_id)\
             .order_by(models.ConversationLog.timestamp.desc())\
             .limit(limit)\
             .all()


def create_event(db: Session, event_data: dict):
    event = models.CalendarEvent(**event_data)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_events_for_user(db: Session, user_id: str):
    return db.query(models.CalendarEvent).filter(models.CalendarEvent.user_id == user_id).order_by(models.CalendarEvent.start_time).all()

from app.db import models
from sqlalchemy.orm import Session
from datetime import datetime

def save_conversation(db: Session, user_id: str, user_message: str, bot_response: str,
                      topic: str, status: str, timestamp: datetime):
    conversation = models.ConversationLog(
        user_id=user_id,
        role='user',  # or 'assistant' based on how you're saving — consider two separate inserts
        message=user_message,
        topic=topic,
        status=status,
        timestamp=timestamp
    )
    db.add(conversation)

    # Optionally also log assistant reply
    assistant_log = models.ConversationLog(
        user_id=user_id,
        role='assistant',
        message=bot_response,
        topic=topic,
        status=status,
        timestamp=timestamp
    )
    db.add(assistant_log)

    db.commit()
    return assistant_log  # or return both if you want
