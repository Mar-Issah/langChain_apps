import streamlit as st
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import FAISS

os.environ.get("OPENAI_API_KEY")

if __name__ == "__main__":
    # 1. Load/Ingest the data
    loader = CSVLoader(
    file_path="./myData.csv",
    csv_args={
        "delimiter": ",",
        "quotechar": '"',
        "fieldnames": ["Words"],
    })

    data = loader.load()
    print(data)

    # 2. embed the data into FAISS vector store, We are not splitting into chunks since it is a small data
    # initiate the embedding
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(data, embeddings)

    # Query the database
    def sim_search(query):
        docs = db.similarity_search(query)
        print(docs)

