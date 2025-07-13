import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

# Load .env variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def get_chat_response(user_message: str, rag_context: str = "", history: List[Dict] = []) -> str:
    messages = [{"role": "system", "content": "You are a helpful real estate assistant."}]
    for turn in history:
        messages.append({"role": turn["role"], "content": turn["message"]})

    # RAG + user message
    messages.append({"role": "user", "content": f"{rag_context}\n\n{user_message}"})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response.choices[0].message.content.strip()


def build_prompt(rag_context: str, user_message: str, history: List[Dict]) -> List[Dict]:
    """
    Combines system instruction, RAG context, user message, and previous history into a prompt.
    """
    messages = []

    messages.append({
        "role": "system",
        "content": "You are a helpful assistant for Okada & Company in the commercial real estate sector. Answer user queries using the knowledge base and past chat history."
    })

    if rag_context:
        messages.append({
            "role": "system",
            "content": f"Relevant document context:\n{rag_context}"
        })

    messages.extend(history)

    messages.append({
        "role": "user",
        "content": user_message
    })

    return messages
