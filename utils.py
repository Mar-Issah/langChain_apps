from langchain.vectorstores import LanceDB, Pinecone as pc
from langchain.llms import OpenAI
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.schema import Document
import pinecone
from pinecone import Pinecone
from pypdf import PdfReader
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import HuggingFaceHub
import time
import os
import lancedb


PINECONE_API_KEY=os.environ["PINECONE_API_KEY"]

#Extract Information from PDF file
def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text



# iterate over files in
# that user uploaded PDF files, one by one
def create_docs(user_pdf_list, unique_id):
    docs=[]
    # each pdf file is a doc. We are creating our own Document with it
    for filename in user_pdf_list:

        chunks=get_pdf_text(filename)

        #Adding items to our list - Adding data & its metadata
        docs.append(Document(
            page_content=chunks,
            metadata={"name": filename.name,"id":filename.file_id,"type=":filename.type,"size":filename.size,"unique_id":unique_id},
        ))

    return docs # Document chunks list


#Create embeddings instance
def create_embeddings_load_data():
    #embeddings = OpenAIEmbeddings()
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings

# push to lancedb
def push_to_lancedb(embeddings):
    db = lancedb.connect("/lancedb")
    # sample data which will be overwritten when ne dos are uploaded
    table = db.create_table(
        "resumes",
        data=[
            {
                "vector": embeddings.embed_query("Hello World"),
                "text": "Hello World",
                "id": "1",
            }
        ],
        mode="overwrite",
    )
    return table

def pull_from_lancedb(table, embeddings, docs):
    docsearch = LanceDB.from_documents(documents=docs, embedding = embeddings, connection=table)
    return docsearch

def similar_docs_lancedb(query, table, embeddings, docs):
  docsearch = pull_from_lancedb(table, embeddings, docs)
  similar_docs = docsearch.similarity_search(query)
  print(similar_docs)
  return similar_docs


#Function to push data to Vector Store - Pinecone here
# Pinecone has eliminated .init method
def push_to_pinecone(pinecone_index_name,embeddings,docs):
    Pinecone(api_key=PINECONE_API_KEY)
    index_name = pinecone_index_name
    index = pc.from_documents(docs, embeddings, index_name=index_name)
    return index


#Function to pull infrmation from Vector Store - Pinecone here
def pull_from_pinecone(pinecone_index_name,embeddings):
   # Pinecone has eliminated .init method
    Pinecone(api_key=PINECONE_API_KEY)
    index = pc.from_existing_index(pinecone_index_name, embeddings)
    return index



#Function to help us get relavant documents from vector store - based on user input
def similar_docs_pinecone(query, k, pinecone_index_name, embeddings, unique_id):
    # Pinecone has eliminated .init method
    Pinecone(api_key=PINECONE_API_KEY)
    index = pull_from_pinecone(pinecone_index_name,embeddings)
    # similarity_search_with_score returns with score % assign to each seacrh doc
    similar_docs = index.similarity_search_with_score(query, int(k),{"unique_id":unique_id})
    # similar_docs = index.similarity_search(query, filter = {"unique_id":unique_id})
    return similar_docs


# Helps us get the summary of a document
def get_summary(current_doc):
    llm = OpenAI(temperature=0)
    #llm = HuggingFaceHub(repo_id="bigscience/bloom", model_kwargs={"temperature":1e-10})
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run([current_doc])
    return summary
