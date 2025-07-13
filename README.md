# RAGent
Multi-Agentic Conversational AI System : A RAG + CRM-enabled conversational assistant to capture, store, and retrieve user information throughout the chat interaction.

## 📊 Architecture (Mermaid)

<img width="3840" height="1714" alt="Untitled diagram _ Mermaid Chart-2025-07-13-204052" src="https://github.com/user-attachments/assets/eb61b363-035a-4df2-8645-4975d4d3d431" />


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
