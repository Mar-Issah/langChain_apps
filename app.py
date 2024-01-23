# fixes a bug with asyncio and jupyter
import nest_asyncio
import asyncio
import os
from langchain.document_loaders.sitemap import SitemapLoader
from langchain_community.document_loaders import WebBaseLoader
import urllib3
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv


load_dotenv()
nest_asyncio.apply()

# sitemap_loader = SitemapLoader( "https://jobs.excelcult.com/wp-sitemap-posts-post-1.xml", default_parser="lxml")
# sitemap_loader.requests_per_second = 2
# sitemap_loader.requests_kwargs = {'verify': False}
# docs = sitemap_loader.load()
# print(docs)



loader = SitemapLoader("https://weworkremotely.com/sitemap.xml")

loader.requests_kwargs = {'verify': './cacert.pem'}
docs = loader.load()
print(docs)


loader = WebBaseLoader("https://weworkremotely.com/sitemap.xml")
# print(loader)
# loader.requests_kwargs = {'verify':False}
# loader.default_parser = "xml"
# data = loader.load()
#print(data)
# text_splitter = RecursiveCharacterTextSplitter(
# chunk_size = 1000,
# chunk_overlap  = 200,
# length_function = len,
# )
# docs_chunks = text_splitter.split_documents(data)
# embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
# db = Chroma.from_documents(docs_chunks, embeddings)
# retriever = db.as_retriever(search_kwargs={"k": 2})
# docs = retriever.get_relevant_documents("engineer")
# print(docs)