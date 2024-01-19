import streamlit as st
from main import get_response, chain
from langchain_community.document_loaders import PyPDFLoader
import os


if __name__ == "__main__":
     st.set_page_config(page_title="Chat GPT Clone",
                              page_icon='📖',
                              layout='centered',
                              )

     st.markdown("<h3 style='text-align: center;'>How can I assist you?/h3>", unsafe_allow_html=True)


     uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"])
     if uploaded_file is not None:
          try:
               # Save the file locally with the original file name and extension
               file_name, file_extension = os.path.splitext(uploaded_file.name)
               file_path = os.path.join(os.getcwd(), uploaded_file.name)

               st.toast(f"File saved as {uploaded_file.name}", icon='😍')

               # Process the file based on its extension
               with st.spinner("Processing..."):
                    if uploaded_file:
                         retriever = get_response(f'./{uploaded_file.name}')
                         query = st.text_input("Please ask your question")
                         relevant_docs = retriever.get_relevant_documents(query)
                         response = chain.run(input_documents=relevant_docs, question=query)
                         submit_btn = st.button("Submit", key="submit", type="secondary")

                         if submit_btn:
                              st.subheader(":green[Answer:]")
                              st.success(response)
                    else:
                         st.warning("Unsupported file type. Only PDF and TXT are supported.")

          except Exception as e:
               st.error(f"Error: {e}")

