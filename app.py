import streamlit as st
from chatbot.chatbot_logic import setup_chatbot
from chatbot.utils import show_loading_message, format_response, clear_chat

# ===== Page Configuration =====
st.set_page_config(page_title="Health Chatbot", page_icon="🤖", layout="centered")

# ===== Sidebar Content =====
with st.sidebar:
    st.title("🩺 Health Insurance AI Chatbot")
    st.write("""
    This AI-powered chatbot assists with health insurance queries by providing fast, reliable, and accurate information.

    **Powered by:**  
    - Langchain Retrieval QA  
    - FAISS Vector Search  
    - OpenAI's Language Model  
    """)
    st.info("Ask your health insurance-related questions below!")

# ===== Main App Logic =====
st.title("🤖 Health Insurance AI Chatbot")

qa_chain = setup_chatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

def has_phrase_overlap(answer, documents, min_overlap=1):
    """
    Show sources only if enough phrases from retrieved docs appear in the answer.
    """
    answer = answer.lower()
    phrases = set()

    for doc in documents:
        text = doc.page_content.lower()
        sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 10]
        phrases.update(sentences)

    common = [phrase for phrase in phrases if phrase in answer]
    return len(common) >= min_overlap

# === Display chat history ===
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# === Chat Input with Immediate Display ===
if user_input := st.chat_input("Ask your health insurance question here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    show_loading_message("Generating response...")
    response = qa_chain.invoke({
        "question": user_input,
        "chat_history": st.session_state.history
    })
    answer_text = response.get("answer", "No answer returned.")
    formatted_response = format_response(answer_text)

    source_files = set()
    if "source_documents" in response:
        for doc in response["source_documents"]:
            source_files.add(doc.metadata.get("source", "Unknown"))

    if source_files and has_phrase_overlap(answer_text, response.get("source_documents", [])):
        formatted_response += "\n\n_Source(s):_\n"
        for src in source_files:
            filename = src.split("/")[-1]
            formatted_response += f"- {filename}\n"

    st.session_state.messages.append({"role": "assistant", "content": formatted_response})
    st.session_state.history.append((user_input, answer_text))
    st.chat_message("assistant").write(formatted_response)

# === Suggested Follow-Up Questions ===
suggestions = ["What does Optical Extras cover?", "Is Ambulance included?", "What does Hospital cover include?"]

st.write("💡 Suggested Questions:")
for question in suggestions:
    if st.button(question):
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("user").write(question)

        show_loading_message("Generating response...")
        response = qa_chain.invoke({
            "question": question,
            "chat_history": st.session_state.history
        })
        answer_text = response.get("answer", "No answer returned.")
        formatted_response = format_response(answer_text)

        source_files = set()
        if "source_documents" in response:
            for doc in response["source_documents"]:
                source_files.add(doc.metadata.get("source", "Unknown"))

        if source_files and has_phrase_overlap(answer_text, response.get("source_documents", [])):
            formatted_response += "\n\n_Source(s):_\n"
            for src in source_files:
                filename = src.split("/")[-1]
                formatted_response += f"- {filename}\n"

        st.session_state.messages.append({"role": "assistant", "content": formatted_response})
        st.session_state.history.append((question, answer_text))
        st.chat_message("assistant").write(formatted_response)

# === Clear Chat with Immediate Rerun ===
st.divider()
if st.button("🗑️ Clear Chat", help="Clear chat history and start fresh"):
    clear_chat()
    st.experimental_rerun()
