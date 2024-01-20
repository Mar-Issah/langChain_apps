from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
import os
from langchain.chains.question_answering import load_qa_chain
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.llms import OpenAI, HuggingFaceHub
from langchain.chains import LLMChain, SimpleSequentialChain, LLMRequestsChain
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from pprint import pprint



os.environ.get("OPENAI_API_KEY")

llm = OpenAI(temperature=0.9)

#This time we are not loading but Reading from the document and saving it in a data var
with open("./jj_sample.txt") as f:
    data = f.read()

#When it comes to document processing, breaking a large document into smaller, more manageable chunks is essential
# Split text
text_splitter = CharacterTextSplitter()
texts = text_splitter.split_text(data)

# Create multiple documents - we got two documents
docs = [Document(page_content=t) for t in texts]
# print(docs)

# load_summarize_chain is a Utility chain
# To create an instance of load_summarizer_chain, we need to provide three arguments. irstly, we need to pass the desired large language model that will be used to query the user input. Secondly, we specify the type of langchain chain to be used for summarizing documents. Lastly, we can set the verbose argument to True if we want to see all the intermediate steps involved in processing the user request and generating the output.
# map reduce summarizes each docs and add all together
chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=False)
chain.run(docs)

# ANOTHER Utility chain LLMRequestsChain. Chain that takes in another chain
# Perform HTTP request using LLMRequestsChain
template = """
Extract the answer to the question '{query}' or say "not found" if the information is not available.
{requests_result}
"""

PROMPT = PromptTemplate(
    input_variables=["query", "requests_result"],
    template=template,
)

llm=OpenAI()
# Utility chain LLMRequestsChain. Chain that takes in another chain
chain = LLMRequestsChain(llm_chain=LLMChain(llm=llm, prompt=PROMPT),verbose=True)

question = "What is the capital of Ghana?"
inputs = {
    "query": question,
    "url": "https://www.google.com/search?q=" + question.replace(" ", "+"),
}
print(chain(inputs))