#from langchain import OpenAI  #Langchain has recently suggested to use the below import
# from langchain.llms import OpenAI
from langchain_openai import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (
ConversationSummaryMemory)
import streamlit as st
import os

os.environ.get("OPENAI_API_KEY")

def get_response(userInput):
    if st.session_state['conversation'] is None:
        llm = OpenAI(
            temperature=0,
            model_name='gpt-3.5-turbo-instruct'  # 'text-davinci-003' model is depreciated now
        )
        # same as creating the conversation var. but in the state
        st.session_state['conversation'] = ConversationChain(
            llm=llm,
            verbose=True,
            memory=ConversationSummaryMemory(llm=llm)
        )

    response = st.session_state['conversation'].predict(input=userInput)
    # print(st.session_state['conversation'].memory.buffer) the summary
    return response
