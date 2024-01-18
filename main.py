from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.llms import HuggingFaceHub
import os
from langchain.chains.question_answering import load_qa_chain


os.environ.get("OPENAI_API_KEY")
os.environ.get("HUGGINGFACEHUB_API_TOKEN")

# Load Documents
# Use the PyPDFDirectoryLoader to load all pdfs in the dir and save it in one document file
def load_doc(file):
	# loader = PyPDFDirectoryLoader(dir)
	_file_name, file_extension = os.path.splitext(file)
	if file_extension.lower() == ".pdf":
		loader = PyPDFLoader(file)
	else:
		loader = TextLoader(file)
	documents = loader.load()
	return documents

# Tranform Documents
def split_doc(docs, chunk_size = 1000, chunk_overlap = 20):
	text_splitter = RecursiveCharacterTextSplitter (chunk_size=chunk_size,
	chunk_overlap= chunk_overlap)
	texts = text_splitter.split_documents(docs)
	return texts

# 3 . Text embedding
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2") # from hugging face which is free
result = embeddings.embed_query("My name is Marsiya")


llm = HuggingFaceHub(repo_id="bigscience/bloom", model_kwargs={"temperature":1e-10})
chain = load_qa_chain(llm, chain_type="stuff")

def get_response(file):
	docs = load_doc(file)
	texts = split_doc(docs)
	db = Chroma.from_documents(texts, embeddings)
	retriever = db.as_retriever(search_kwargs={"k": 2})
	return retriever
