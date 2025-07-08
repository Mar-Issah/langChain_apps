import os
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS

os.environ.get("OPENAI_API_KEY")


# 1. Load/Ingest the data
loader = CSVLoader(
file_path="./myData.csv",
csv_args={
    "delimiter": ",",
    "quotechar": '"',
    "fieldnames": ["Words"],
})

data = loader.load()

# 2. embed the data into FAISS vector store, We are not splitting into chunks since it is a small data
# initiate the embedding
# embeddings = OpenAIEmbeddings()
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
db = FAISS.from_documents(data, embeddings)

# Query the FAISS vector database
def sim_search(query):
    docs = db.similarity_search(query)
    return docs
