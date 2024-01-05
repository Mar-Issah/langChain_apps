from langchain.llms import HuggingFaceHub
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

os.environ.get("OPENAI_API_KEY")

def answer_query(query):
  llm = ChatOpenAI(model_name="gpt-3.5-turbo",temperature= 0)
  response = llm(query)
  return response
