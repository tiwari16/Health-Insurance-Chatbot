from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from .vectorstore import load_vectorstore
from .config import OPENAI_API_KEY

def setup_chatbot():
    db = load_vectorstore()
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())
    return qa_chain
