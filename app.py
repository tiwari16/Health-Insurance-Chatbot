import streamlit as st
from chatbot.chatbot_logic import setup_chatbot
from chatbot.utils import show_loading_message, format_response, clear_chat

# ===== Page Configuration =====
st.set_page_config(page_title="AU Health Chatbot", page_icon="🤖", layout="centered")

# ===== Sidebar Content =====
with st.sidebar:
    st.title("🩺 Australian Unity AI Chatbot")
    st.write("""
    This AI-powered chatbot assists with health insurance queries by providing fast, reliable, and accurate information.

    **Powered by:**  
    - Langchain (RAG)  
    - FAISS Vector Search  
    - OpenAI's Language Model  
    
    Feel free to ask your health-related questions or general inquiries.
    """)
    st.info("Built with Australian Unity's brand colours and a focus on enhancing customer experience.")

# ===== Main Chatbot App =====
st.title("🤖 Health Insurance AI Chatbot")

qa_chain = setup_chatbot()

# Initialise chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User Input
if user_input := st.chat_input("Ask a health insurance question..."):
    st.session_state.messages.append({"role": "user", "content": user_input})

    show_loading_message("Generating a response...")

    response = qa_chain.run(user_input)
    formatted_response = format_response(response)

    st.session_state.messages.append({"role": "assistant", "content": formatted_response})
    st.chat_message("assistant").write(formatted_response)

# Divider and Clear Chat Button
st.divider()
if st.button("🗑️ Clear Chat", help="Clear chat history and start fresh"):
    clear_chat()
