import whisper
# from langchain.llms import OpenAI
from langchain_openai import OpenAI
from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits import ZapierToolkit
from langchain_community.utilities.zapier import ZapierNLAWrapper
import os

os.environ.get("OPENAI_API_KEY")
os.environ.get("ZAPIER_NLA_API_KEY")

def email_summary(file):
    llm = OpenAI(temperature=0)
    print("email_summary")
    # Initializing zapier
    llm = OpenAI(temperature=0)
    zapier = ZapierNLAWrapper()
    toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
    agent = initialize_agent(
    toolkit.get_tools(), llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    # specify a model, here its BASE
    model = whisper.load_model("base")

    # transcribe audio file
    result = model.transcribe(file)
    print(result["text"])

    # Send email using zapier
    agent.run("Send an Email to masy370@gmail.com via gmail summarizing the following text provided below : "+result["text"])

