# from langchain.vectorstores import Pinecone as pc
from pinecone import Pinecone
from langchain_openai import OpenAI
from langchain_core.documents import Document
from typing import List
from langchain_core.vectorstores import VectorStore
from langchain_pinecone import PineconeVectorStore
import os
from langchain_huggingface import HuggingFaceEmbeddings
import streamlit as st
from langchain.chains.summarize import load_summarize_chain
import getpass
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
hf_api_key = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
pinecone_index_name = "hr-screening"
# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)

# vector_store = st.session_state.get("vector_store")


def create_store():
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        # print(embeddings)
        # This can be configure on Pinecone dashboard. uncomment below to create a new index
        # pc.create_index(
        #     name="hr-screening",
        #     dimension=384,
        #     metric="cosine",  # or 'dotproduct'/'euclidean' based on your use case
        # )
        index = pc.Index(pinecone_index_name)
        vector_store = PineconeVectorStore(index=index, embedding=embeddings)
        return vector_store
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None


def pull_from_pinecone(vector_store, job_desc, k) -> VectorStore:
    """
    Pull documents from Pinecone vector store.

    Args:
        embeddings: Embeddings instance.

    Returns:
        PineconeVectorStore: Vector store.
    """
    try:
        results = vector_store.similarity_search_with_score(job_desc, k=k)
        return results
    except Exception as e:
        print(e)


def push_to_pinecone(vector_store, docs: List[Document]) -> None:
    """
    Push documents to Pinecone vector store.

    Args:
        docs (list): List of documents.

    Returns:
        PineconeVectorStore: Vector store.
    """
    try:
        vector_store.add_documents(documents=docs)
        return True
    except Exception as e:
        print(e)


# Helps us get the summary of a document/resume
def get_summary(current_doc):
    llm = OpenAI(temperature=0.4)
    # llm = HuggingFaceHub(repo_id="bigscience/bloom", model_kwargs={"temperature":1e-10})
    chain = load_summarize_chain(llm, chain_type="stuff")
    summary = chain.run([current_doc])
    return summary


# push to lancedb
# def push_to_lancedb(embeddings):
#     db = lancedb.connect("/lancedb")
#     # sample data which will be overwritten when ne dos are uploaded
#     table = db.create_table(
#         "resumes",
#         data=[
#             {
#                 "vector": embeddings.embed_query("Hello World"),
#                 "text": "Hello World",
#                 "id": "1",
#             }
#         ],
#         mode="overwrite",
#     )
#     return table


# def pull_from_lancedb(table, embeddings, docs):
#     docsearch = LanceDB.from_documents(
#         documents=docs, embedding=embeddings, connection=table
#     )
#     return docsearch


# def similar_docs_lancedb(query, table, embeddings, docs):
#     docsearch = pull_from_lancedb(table, embeddings, docs)
#     similar_docs = docsearch.similarity_search(query)
#     return similar_docs
