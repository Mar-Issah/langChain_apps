# fixes a bug with asyncio and jupyter
import nest_asyncio
import asyncio
import os
from langchain.document_loaders.sitemap import SitemapLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
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



loader = SitemapLoader("https://jobs.apple.com/sitemap/sitemap-jobs-en-gb.xml")

loader.requests_kwargs = {'verify': False}
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
chunk_size = 1000,
chunk_overlap  = 200,
length_function = len,
)
docs_chunks = text_splitter.split_documents(docs)
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
# load it into Chroma
db2 = Chroma.from_documents(docs_chunks, embeddings, persist_directory="./chroma_db")
print('done...')


# db3=Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
# docs = db3.similarity_search("software developers from countries that emphasize learning a second language")
# print(docs)

