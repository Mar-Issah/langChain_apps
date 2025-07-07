#from langchain_huggingface import HuggingFaceHub
import os
from langchain_openai import OpenAI
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

# os.environ.get("HUGGINGFACEHUB_API_TOKEN")
os.environ.get("OPENAI_API_KEY")
os.environ.get("GOOGLE_API_KEY")

def answer_query(query):
  #llm = OpenAI(model_name="gpt-4o-mini",temperature=0.5)
  llm = GoogleGenerativeAI(model="gemini-2.0-flash")

  #llm = HuggingFaceHub(repo_id = "google/flan-t5-large")
  response = llm.invoke(query)
  return response
