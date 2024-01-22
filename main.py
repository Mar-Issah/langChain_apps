import os
from langchain_community.llms import OpenAI
#from langchain.llms import OpenAI
#The above is no longer avialable, so replaced it with the below import
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.tools import DuckDuckGoSearchRun


os.environ.get("OPENAI_API_KEY")

def get_script(prompt, video_length, temperature):
    # Template for generating 'Title' based on the topic of the user
    title_template = PromptTemplate(
        input_variables = ['subject'],
        template='Please come up with a title for a YouTube video on {subject}.'
        )

    # Template for generating 'Video Script' using DuckDuckGo search engine
    # Please install DuckDuckGo
    script_template = PromptTemplate(
        input_variables = ['title', 'DuckDuckGo_Search','duration'],
        template='Create a script for a YouTube video based on this title. TITLE: {title} of duration: {duration} minutes using this search data {DuckDuckGo_Search} '
    )
        #Setting up OpenAI LLM
    llm = ChatOpenAI(temperature=temperature, model_name='gpt-3.5-turbo')

    #Creating chains for 'Title' & 'Video Script'
    title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True)
    script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True)

    # https://python.langchain.com/docs/modules/agents/tools/integrations/ddg
    search = DuckDuckGoSearchRun()

    # Executing the chains we created for 'Title'
    title = title_chain.run(prompt)

    # Executing the chains we created for 'Video Script' by taking help of search engine 'DuckDuckGo'
    search_result = search.run(prompt)
    script = script_chain.run(title= title, DuckDuckGo_Search= search_result, duration=video_length)

    # Returning the output
    return search_result, title, script

