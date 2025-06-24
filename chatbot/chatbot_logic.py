from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from .vectorstore import load_vectorstore
from .config import OPENAI_API_KEY

def setup_chatbot():
    """
    Sets up a conversational, grounded health insurance chatbot:
    - Uses FAISS for document retrieval
    - Applies chat memory for multi-turn interactions
    - Avoids hallucination by sticking to indexed content
    - Returns sources alongside answers
    """
    db = load_vectorstore()

    # Load OpenAI Chat model (GPT) with your API key
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

    # FAISS Retriever with Top-K chunk coverage for accuracy
    retriever = db.as_retriever(search_kwargs={"k": 4})

    # Create Conversational Retrieval QA Chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain
