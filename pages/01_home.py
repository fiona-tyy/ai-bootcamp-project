import streamlit as st
from helper_functions import llm # <--- This is the helper function that we have created 🆕
from logics.customer_query_handler import process_user_message
from openai import OpenAI, OpenAIError
import os
from dotenv import load_dotenv

load_dotenv()  # reads .env from the folder you run streamlit from


SYSTEM_PROMPT = """You are a helpful, calm and respectful assistant on a website about \
divorce proceedings at the Syariah Court in Singapore.

Your role:
- Explain the general process, terminology (e.g. talak, khuluk, fasakh, taklik, \
iddah, nafkah, mutaah, harta sepencarian) and what people can expect at each stage.
- Help people understand what questions to ask and what documents they may need.
- Point people to official sources: the Syariah Court Singapore, the Registry of \
Muslim Marriages (ROMM), MUIS, and the Family Justice Courts where relevant.

Rules:
- You give general information, not legal advice. When a question depends on someone's \
specific circumstances, say so and suggest consulting a lawyer or the Syariah Court.
- Procedures, forms and fees change. If you are unsure whether something is current, \
say so and suggest checking the official Syariah Court website.
- Never invent laws, section numbers, fees or deadlines.
- People asking may be going through a hard time. Be kind and non-judgmental.
- If someone mentions violence, abuse or danger, encourage them to seek help \
immediately (Police: 999) and mention that family violence support services exist.
- Keep answers clear and reasonably concise. Use plain language.
"""

WELCOME = (
    "Assalamualaikum and welcome. I can explain how divorce proceedings at the "
    "Syariah Court generally work, what common terms mean, and where to find help. "
    "What would you like to know?"
)

SUGGESTIONS = [
    "What are the main types of Muslim divorce?",
    "What happens at the first court session?",
    "Do I need a lawyer?",
    "What is harta sepencarian?",
]


@st.cache_resource
def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


MODEL = os.getenv("OPENAI_MODEL")


st.title("⚖️ Syariah Court Divorce Proceedings")
st.write("Ask our AI assistant questions about the divorce process.")
st.info(
    "The assistant gives general information only and may make mistakes. "
    "It is not a substitute for legal advice.",
    icon="ℹ️",
)

client = get_client()
if client is None:
    st.error(
        "No API key found. Add `OPENAI_API_KEY` to your `.env` file."
    )
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message (not sent to the model)
with st.chat_message("assistant"):
    st.markdown(WELCOME)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Suggested questions, only before the first message
pending = None
if not st.session_state.messages:
    cols = st.columns(2)
    for i, q in enumerate(SUGGESTIONS):
        if cols[i % 2].button(q, use_container_width=True, key=f"sugg_{i}"):
            pending = q

typed = st.chat_input("Type your question...")
prompt = typed or pending

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=MODEL,
                max_completion_tokens=2048,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}]
                + st.session_state.messages,
                stream=True,
            )
            reply = st.write_stream(stream)
        except OpenAIError as e:
            reply = None
            st.error(f"Sorry, something went wrong contacting the assistant: {e}")

    if reply:
        st.session_state.messages.append({"role": "assistant", "content": reply})
    else:
        # Drop the unanswered question so history stays valid
        st.session_state.messages.pop()

if st.session_state.messages:
    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()
