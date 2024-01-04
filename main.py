from langchain.llms import HuggingFaceHub
import os
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

api_keys = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
# api_keys=os.environ.get("OPENAI_API_KEY")

def answer_query(query):
  llm = OpenAI(model_name="gpt-3.5-turbo-instruct",temperature=0)
  # options = {"wait_for_model": True, "use_gpu": False}
  # llm = HuggingFaceHub(repo_id = "google/flan-t5-large")
  response = llm(query)
  return response
