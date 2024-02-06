import streamlit as st
from utils import *
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from io import StringIO

if __name__ == '__main__':
   st.title("Let's do code review for your python code")
   st.header("Please upload your .py file here:")

   # Capture the .py file data
   data = st.file_uploader("Upload python file",type=".py")

   if data:
        # Create a StringIO object and initialize it with the decoded content of 'data'
    stringio = StringIO(data.getvalue().decode('utf-8'))
    fetched_data = stringio.read()

    # Initialize a ChatOpenAI instance with the specified model
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9)

    # Create a SystemMessage instance with the specified content, providing information about the assistant's role.
    systemMessage = SystemMessage(content="You are a code review assistant. Provide detailed suggestions to improve the given Python code along by mentioning the existing code line by line with proper indent")

    # Create a HumanMessage instance with content read from some data source.
    humanMessage = HumanMessage(content=fetched_data)

    finalResponse = chat([systemMessage, humanMessage])

    #Display review comments
    st.markdown(finalResponse.content)
    text_downloader(finalResponse.content)
