import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.schema import Document

# --- Page Config ---
st.set_page_config(
    page_title="AU Health Cover Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar UI ---
with st.sidebar:
    st.title("🩺 Health Insurance Chatbot")
    st.markdown("""
    This chatbot answers member questions about **hospital and extras cover**, 
    using product fact sheets from health insurance.

    💡 **Built with RAG** (Retrieval-Augmented Generation)  
    🔍 Queries real policy docs  
    🤖 Powered by **OpenAI GPT** and **LangChain**
    """)
    if st.button("🔄 Clear chat"):
        st.session_state.messages = []

# --- OpenAI Key ---
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OpenAI API key missing. Please add it to .streamlit/secrets.toml or set as an env variable.")
    st.stop()
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# --- Fake Documents for Demo ---
docs = [
    Document(page_content="Extras cover includes dental, optical, and physio."),
    Document(page_content="Gold hospital cover includes private room and ambulance cover."),
    Document(page_content="Claims can be submitted online or through the mobile app."),
    Document(page_content="Update your bank details in Account Settings."),
    Document(page_content="Direct debit setup is available under billing preferences."),
    Document(page_content="Lapsed policies can be reactivated within 60 days online."),
]

# --- Embeddings + FAISS Vectorstore ---
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)

# --- Build RAG Chain ---
llm = ChatOpenAI(model="gpt-3.5-turbo")
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_type="similarity", k=2),
    return_source_documents=True
)

# --- Chat Section ---
st.title("🤖 Health Insurance Assistant")
st.caption("Ask me anything about your health insurance cover.")

# --- Initialise chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Render previous messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat input ---
user_input = st.chat_input("Type your question here...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Searching policy documents..."):
            response = qa(user_input)
            answer = response['result']
            source = response['source_documents'][0].page_content
            st.markdown(answer)
            with st.expander("📄 Source document used"):
                st.code(source)

    st.session_state.messages.append({"role": "assistant", "content": answer})
