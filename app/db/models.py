from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    company = Column(String)
    email = Column(String)

class ConversationLog(Base):
    __tablename__ = "conversation_logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    role = Column(String)  # 'user' or 'assistant'
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    topic = Column(String, nullable=True)       # e.g. 'Leasing', 'Pricing'
    status = Column(String, nullable=True)      # e.g. 'Resolved', 'Unresolved'

class CalendarEvent(Base):
    __tablename__ = "calendar_events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    title = Column(String)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
