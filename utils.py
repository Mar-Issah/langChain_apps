# from langchain.llms import OpenAI
from langchain_openai import OpenAI
import os
import time
import base64
import streamlit as st

os.environ.get("OPENAI_API_KEY")

# Function to download text content as a file using Streamlit
def text_downloader(raw_text):
    # Generate a timestamp for the filename to ensure uniqueness
    timestr = time.strftime("%Y%m%d-%H%M%S")

    # Encode the raw text in base64 format for file download
    b64 = base64.b64encode(raw_text.encode()).decode()

    new_filename = "code_review_analysis_file_{}_.txt".format(timestr)

    st.markdown("#### Download File ✅###")

    href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click Here!!</a>'

  # Display the HTML link using Streamlit markdown
    st.markdown(href, unsafe_allow_html=True)

