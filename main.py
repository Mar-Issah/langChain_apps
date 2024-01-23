import os
import asyncio
from langchain.document_loaders.sitemap import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
import streamlit as st


os.environ.get("HUGGINGFACEHUB_API_TOKEN")

#Function to fetch data from website
#https://python.langchain.com/docs/modules/data_connection/document_loaders/integrations/sitemap
def get_website_data(sitemap_url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loader = SitemapLoader(sitemap_url)
    loader.requests_kwargs = {'verify': './cacert.pem'}
    docs = loader.load()
    # print(docs)
    return docs

#Function to split data into smaller chunks
def split_data(docs):
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
    )
    docs_chunks = text_splitter.split_documents(docs)
    # print(docs_chunks)
    return docs_chunks

#Function to create embeddings instance
def create_embeddings():
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings

# Function to push data to Chroma
def push_to_chroma(embeddings, chunk_data):
    Chroma.from_documents(chunk_data, embeddings, persist_directory="./chroma_db")

# Function to pull data from chroma
def pull_from_chroma(query):
    db = Chroma(persist_directory="./chroma_db", embedding_function= create_embeddings())
    docs = db.similarity_search(query)
    return docs


