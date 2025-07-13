import streamlit as st
import requests

def local_css(css):
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

local_css("""
    div[data-testid="stTextInput"] > div > div > input {
        background-color: #111;
        color: #fff;
        border: 1px solid #333;
        padding: 0.6em;
    }
    div[data-testid="stChatMessage"] {
        background-color: #1a1a1a;
        padding: 1em;
        border-radius: 10px;
        margin-bottom: 0.5em;
    }ççç
    .stButton>button {
        background-color: #D4AF37;
        color: black;
        font-weight: bold;
        border: none;
        padding: 0.5em 1em;
        border-radius: 8px;
    }
""")

API_URL = "http://127.0.0.1:8000"  # update if deployed

st.set_page_config(page_title="Okada AI Assistant", layout="centered")

st.markdown(
    "<h1 style='text-align: center; color: #D4AF37;'>🏢 Okada AI Assistant</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: #CCCCCC;'>Your real estate knowledge partner powered by AI</p>",
    unsafe_allow_html=True
)

if "history" not in st.session_state:
    st.session_state.history = []

user_id = st.text_input("User ID", value="dheeraj01")

# --- Chat Section ---
st.subheader("Chat with RAG + CRM Bot")
with st.form("chat_form", clear_on_submit=True):
    message = st.text_input("Enter your message:")
    submitted = st.form_submit_button("Send")

    if submitted and message:
        payload = {
            "user_id": user_id,
            "message": message,
            "history": st.session_state.history
        }
        res = requests.post(f"{API_URL}/chat", json=payload)
        if res.status_code == 200:
            reply = res.json()["response"]
            st.session_state.history.append({"role": "user", "content": message})
            st.session_state.history.append({"role": "assistant", "content": reply})
        else:
            st.error("Failed to get response from server.")

# --- Display Chat History ---
for msg in st.session_state.history[::-1]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- File Upload Section ---
st.markdown("---")
st.subheader("📁 Upload Document for RAG")
doc_file = st.file_uploader("Upload a CSV/TXT/JSON file", type=["csv", "txt", "json", "pdf"])
if doc_file:
    res = requests.post(
        f"{API_URL}/upload_docs",
        files={"files": (doc_file.name, doc_file, doc_file.type)}
    )
    if res.status_code == 200:
        st.success(f"{doc_file.name} uploaded and indexed!")
    else:
        st.error("Failed to upload.")
