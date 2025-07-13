from fastapi import FastAPI
from app.apis import chat, upload, crm, reset, calendar
from app.db import models

from app.config import engine
app = FastAPI(
    title="Multi-Agentic Conversational AI System",
    description="A RAG + CRM-enabled conversational assistant to capture, store, and retrieve user information throughout the chat interaction. ",
    version="1.0.0"
)

# Register routers
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(upload.router, prefix="/upload_docs", tags=["RAG"])
app.include_router(crm.router, prefix="/crm", tags=["CRM"])
app.include_router(reset.router, prefix="/reset", tags=["Memory"])
app.include_router(calendar.router, prefix="/calendar", tags=["Calendar"])
models.Base.metadata.create_all(bind=engine)
@app.get("/")
def root():
    return {"message": "Welcome to the Okada CRE Assistant API!"}
