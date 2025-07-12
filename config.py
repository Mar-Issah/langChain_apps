from langchain_openai import ChatOpenAI
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import os
import streamlit as st
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()
os.environ.get("OPENAI_API_KEY")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)


CHROMA_DIR = "./chroma_langchain_db"


def get_vector_store():
    # Check if already in session state
    if "vector_store" not in st.session_state:
        # If dir exists, load the vector store, else create a new one
        if os.path.exists(CHROMA_DIR):
            st.session_state.vector_store = Chroma(
                persist_directory=CHROMA_DIR,
                collection_name="my_collection",
                embedding_function=embeddings,
            )
        else:
            # This will create the directory and save the store when documents are added
            st.session_state.vector_store = Chroma(
                persist_directory=CHROMA_DIR,
                collection_name="my_collection",
                embedding_function=embeddings,
            )
    return st.session_state.vector_store
