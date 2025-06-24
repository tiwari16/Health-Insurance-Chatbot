import time
import streamlit as st

def show_loading_message(message="Processing..."):
    """Displays a temporary loading spinner."""
    with st.spinner(message):
        time.sleep(0.5)  # Small delay for demo purposes


def format_response(response):
    """Formats the chatbot's response (can expand later)."""
    if isinstance(response, str):
        return response.strip()
    return str(response)


def clear_chat():
    """Clears Streamlit chat session."""
    st.session_state.messages = []
