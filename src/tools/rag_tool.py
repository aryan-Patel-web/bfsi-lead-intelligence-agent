import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

def get_vector_store():
    """Get or create the vector store."""
    database_path = "database"
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    if os.path.exists(database_path) and os.listdir(database_path):
        # Use the existing vector store
        vectorstore = Chroma(persist_directory=database_path, embedding_function=embeddings)
    else:
        # Load documents and create a new vector store
        loader = DirectoryLoader("./data/case_studies")
        docs = loader.load()
        vectorstore = Chroma.from_documents(docs, embeddings, persist_directory=database_path)
    
    return vectorstore

def fetch_similar_case_study(description):
    """Fetch the most similar case study to the given description."""
    vectorstore = get_vector_store()
    vectorstore_retreiver = vectorstore.as_retriever(search_kwargs={"k": 1})
    docs = vectorstore_retreiver.invoke(description)
    return docs[0].page_content