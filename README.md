# RAGent
Multi-Agentic Conversational AI System : A RAG + CRM-enabled conversational assistant to capture, store, and retrieve user information throughout the chat interaction.

## 📊 Architecture (Mermaid)

```mermaid
graph TD
  subgraph Client
    U[User]
  end

  subgraph API
    CHAT[Chatbot API - /chat] --> GPT[LLM - OpenAI GPT]
    CHAT --> RAG[RAG Retriever]
    CHAT --> CRM[CRM Logger]
  end

  subgraph RAG_System
    RAG --> FAISS[Vector Store - FAISS]
    RAG --> DOCS[Embedded Docs - /upload_docs]
  end

  subgraph CRM_Database
    CRM --> USERS[Users Table]
    CRM --> LOGS[Conversation Logs]
    CRM --> EVENTS[Calendar Events]
  end

  U --> CHAT

##  Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/RAGent.git
   cd RAGent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file using `.env.example` and fill in your API key.

5. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

6. Open Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 📡 API Endpoints

| Method | Endpoint                        | Description                            |
|--------|----------------------------------|----------------------------------------|
| POST   | `/chat`                          | Send a message and get LLM + RAG reply |
| POST   | `/upload_docs`                   | Upload and index documents             |
| POST   | `/crm/create_user`               | Create a new CRM user                  |
| PUT    | `/crm/update_user`               | Update CRM user info                   |
| GET    | `/crm/conversations/{user_id}`   | Get full chat history for a user       |
| POST   | `/reset`                         | Clear chat history (by user or global) |

## 💬 Example: /chat Request

```json
{
  "user_id": "dheeraj01",
  "message": "What’s the rent for Suite 101?",
  "history": []
}
```

### ✅ Response

```json
{
  "user_id": "dheeraj01",
  "response": "Suite 101 is listed at $42/SF/year for 2,000 SF...",
  "topic": "Pricing",
  "status": "Inquiring",
  "knowledge_used": ["Property: ..."]
}
```

## 🙌 Contributors

- Dheeraj Singh, Shrutika Parab – Backend, LLM Integration, CRM & RAG System
