from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
import os
import pdfplumber

def extract_text_from_pdfs(data_path="data"):
    """Extracts text from PDFs, prints debug info, chunks it, and returns Document objects."""
    documents = []
    splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=50)

    for root, _, files in os.walk(data_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                file_path = os.path.join(root, file)
                try:
                    with pdfplumber.open(file_path) as pdf:
                        text = ""
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"

                    text = text.strip()

                    print(f"\n📄 File: {file_path}")
                    print(f"🔢 Extracted {len(text)} characters")

                    if text:
                        print(f"📝 Extracted Text Preview:\n{text[:500]}...\n")
                        chunks = splitter.split_text(text)
                        for chunk in chunks:
                            documents.append(Document(page_content=chunk, metadata={"source": file_path}))

                        print(f"✅ Loaded {len(chunks)} chunks from: {file_path}\n")
                    else:
                        print(f"⚠️ No extractable text in: {file_path}\n")

                except Exception as e:
                    print(f"⚠️ Skipping {file_path} due to error: {e}\n")

    return documents

def create_text_based_vectorstore(embeddings, data_path="data"):
    """Creates FAISS vectorstore from chunked PDF text."""
    docs = extract_text_from_pdfs(data_path)

    if not docs:
        print("⚠️ No valid documents found. Vectorstore not created.")
        return None

    db = FAISS.from_documents(docs, embeddings)
    db.save_local("faiss_index")
    return db

def load_vectorstore():
    """Loads FAISS index or creates one from PDF text if not present."""
    embeddings = OpenAIEmbeddings()

    if os.path.exists("faiss_index/index.faiss"):
        db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    else:
        db = create_text_based_vectorstore(embeddings)
    
    return db
