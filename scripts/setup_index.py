# scripts/setup_index.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.rag import load_and_index_documents

if __name__ == "__main__":
    load_and_index_documents()
    print("✅ Vector store built and saved.")