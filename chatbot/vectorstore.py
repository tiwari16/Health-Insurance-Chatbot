from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
import os

def load_vectorstore():
    """Loads an existing FAISS vector store if available."""
    embeddings = OpenAIEmbeddings()
    
    # Check if FAISS index exists
    if os.path.exists("faiss_index/index.faiss"):
        db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    else:
        db = create_demo_vectorstore(embeddings)
    return db


def create_demo_vectorstore(embeddings):
    """Creates a vector store with mock documents for demonstration."""
    
    docs = [
        Document(page_content="Extras cover includes dental, optical, and physio."),
        Document(page_content="Gold hospital cover includes private room and ambulance cover."),
        Document(page_content="Claims can be submitted online or through the mobile app."),
        Document(page_content="Update your bank details in Account Settings."),
        Document(page_content="Direct debit setup is available under billing preferences."),
        Document(page_content="Lapsed policies can be reactivated within 60 days online."),
    ]

    db = FAISS.from_documents(docs, embeddings)
    
    # Optional: Save the FAISS index
    db.save_local("faiss_index")
    
    return db
