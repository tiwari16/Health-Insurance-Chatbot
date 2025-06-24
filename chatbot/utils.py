import streamlit as st
import time

def show_loading_message(message="Thinking..."):
    """Displays a temporary loading message."""
    with st.spinner(message):
        time.sleep(0.5)  # Optional short delay for better UI effect

def clear_chat():
    """Clears chat history and resets session state."""
    st.session_state.messages = []
    st.session_state.history = []

def format_response(text):
    """
    Formats chatbot response for clean, easy reading:
    - Converts bullet patterns to consistent markdown
    - Detects common benefit/inclusion phrases for lists
    - Handles semicolon-separated lists from PDF quirks
    - Adds paragraph breaks for structure
    """
    formatted = text.strip()

    # Handle simple semicolon-separated lists
    if ";" in formatted and "\n" not in formatted:
        parts = [p.strip() for p in formatted.split(";") if p.strip()]
        return "\n".join(f"- {p}" for p in parts)

    lines = formatted.split("\n")
    output = []

    for line in lines:
        line = line.strip()

        # Preserve existing list indicators
        if line.startswith(("-", "•", "●", "*", "o")) or line[:2].isdigit():
            output.append(f"- {line.lstrip('-•●*o').strip()}")

        # Force bullet if sentence suggests a list item
        elif any(keyword in line.lower() for keyword in ["includes", "benefits", "covers", "provides", "offers", "services"]):
            output.append(f"- {line}")

        # Break semicolon-separated fragments into bullets
        elif ";" in line:
            parts = [p.strip() for p in line.split(";") if p.strip()]
            output.extend(f"- {p}" for p in parts)

        else:
            output.append(line)

    return "\n\n".join(output)
