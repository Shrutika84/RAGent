import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/chat_crm.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
load_dotenv()

class Settings:
    # OpenAI LLM
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

    # Embedding
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # RAG
    VECTOR_STORE_PATH: str = os.getenv("VECTOR_STORE_PATH", "./data/faiss_index/index.faiss")
    DOC_EMBED_CSV: str = os.getenv("DOC_EMBED_CSV", "./data/HackathonInternalKnowledgeBase.csv")

    # Memory
    MAX_HISTORY_MESSAGES: int = int(os.getenv("MAX_HISTORY_MESSAGES", 5))

settings = Settings()
