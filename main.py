import os
#from langchain import OpenAI  #Langchain has recently suggested to use the below import
from langchain_community.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory,
ConversationSummaryMemory, ConversationBufferWindowMemory)
import tiktoken
from langchain.memory import ConversationTokenBufferMemory
import streamlit as st

os.environ.get("OPENAI_API_KEY")

llm = ChatOpenAI(
    temperature=0,
    model_name='gpt-3.5-turbo'  #'text-davinci-003' - This model has been depreciated
)

conversation = ConversationChain(
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory()  #decide which memory you like
)

#just to see what is being sent to the llm
# print(conversation.prompt.template)
# conversation("Good morning AI")
# conversation("My name is Marsiya")
# print(conversation.json())
# conversation.predict(input="I live in Calgary, Canada")
# print(conversation.memory.buffer)
# conversation.predict(input="What is my name?")


def get_response(userInput, api_key):
    if st.session_state['conversation'] is None:

        llm = OpenAI(
            temperature=0,
            openai_api_key=api_key,
            model_name='gpt-3.5-turbo-instruct'  # 'text-davinci-003' model is depreciated now, so we are using the openai's recommended model
        )

        st.session_state['conversation'] = ConversationChain(
            llm=llm,
            verbose=True,
            memory=ConversationSummaryMemory(llm=llm)
        )

    response=st.session_state['conversation'].predict(input=userInput)
    print(st.session_state['conversation'].memory.buffer)


    return response
