import streamlit as st
from dotenv import load_dotenv
from utils import *


def main():
    load_dotenv()
    st.set_page_config(page_title="Pinecone - Vector Store", page_icon='🎫')
    st.title("Please upload files...📁 ")

    # Upload the pdf file...
    pdf = st.file_uploader("Only PDF files allowed", type=["pdf"])

    # Extract the whole text from the uploaded pdf file
    if pdf is not None:
        with st.spinner('Wait for it...'):
            text=read_pdf_data(pdf)
            st.toast("👉Reading PDF done")

            # Create chunks
            docs_chunks=split_data(text)
            st.write(docs_chunks)
            st.toast("👉Splitting data into chunks done")

            # Create the embeddings
            embeddings=create_embeddings_load_data()
            st.write("👉Creating embeddings instance done")

            # Build the vector store (Push the PDF data embeddings)
            push_to_pinecone("b115c8b2-fca0-4e6f-b0d3-07cc29935642","us-west1-gcp-free","tickets",embeddings,docs_chunks)

        st.success("Successfully pushed the embeddings to Pinecone")


if __name__ == '__main__':
    main()
