import os
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv

load_dotenv()

os.environ.get("OPENAI_API_KEY")


def get_script(topic, video_length, temperature):
    # Setting up OpenAI LLM
    llm = OpenAI(temperature=temperature, model_name="gpt-4o-mini", max_tokens=1000)

    #  DuckDuckGoSearchRun allows you to programmatically perform web searches
    ddg_search = DuckDuckGoSearchRun()

    # Template for generating 'Title' based on the topic of the user
    title_template = PromptTemplate(
        input_variables=["subject"],
        template="Please come up with a title for a YouTube video on {subject}.",
    )

    # Template for generating 'Video Script' using DuckDuckGo search engine
    script_template = PromptTemplate(
        input_variables=["title", "DuckDuckGo_Search", "duration"],
        template="Create a script for a YouTube video based on this title. TITLE: {title} of duration: {duration} minutes using this search data {DuckDuckGo_Search} ",
    )

    # Creating chains for 'Title' & 'Video Script'
    title_chain = LLMChain(llm=llm, prompt=title_template, verbose=False)
    script_chain = LLMChain(llm=llm, prompt=script_template, verbose=False)

    # Executing the chains we created for 'Title'
    title = title_chain.run(topic)

    # Executing the chains we created for 'Video Script' by taking help of search engine 'DuckDuckGo'
    search_result = ddg_search.run(topic)

    script = script_chain.run(
        title=title, DuckDuckGo_Search=search_result, duration=video_length
    )

    # Returning the outputs
    return search_result, title, script
