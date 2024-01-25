from langchain.llms import HuggingFaceHub
import os
# from langchain.llms import OpenAI
#from langchain_community.llms import OpenAI
from langchain_openai import OpenAI

# os.environ.get("HUGGINGFACEHUB_API_TOKEN")
os.environ.get("OPENAI_API_KEY")

def answer_query(query):
  llm = OpenAI(model_name="gpt-3.5-turbo-instruct",temperature=0.5)
  #llm = HuggingFaceHub(repo_id = "google/flan-t5-large")
  response = llm(query)
  return response
