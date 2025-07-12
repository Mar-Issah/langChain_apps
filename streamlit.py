import streamlit as st
from typing import Optional
from langchain.vectorstores.base import VectorStoreRetriever
from file_utils import (
    list_files,
    delete_file,
    select_file,
    extract_id_from_filename,
    upload_file,
)
from config import get_vector_store
from vector_utils import create_retriever, delete_docs_by_original_id
from main import get_chat_response
from langchain_core.messages import HumanMessage, AIMessage


def main():
    st.set_page_config(page_title="RAG", page_icon="📖", layout="centered")

    st.markdown(
        "<h3 style='text-align: center;'>Select a Document to Chat</h3>",
        unsafe_allow_html=True,
    )

    retriever: Optional[VectorStoreRetriever] = None

    vector_store = get_vector_store()
    # print(vector_store)

    try:
        with st.sidebar:
            upload_file()
            st.header("Your Files 📁:")
            directory = "./files"

            file_list = list_files(directory)

            if file_list:
                for filename in file_list:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        # Dynamicaaly change the btn type on click using session_staate
                        st.button(
                            "📄" + filename,
                            key=f"select_{filename}",
                            on_click=select_file,
                            args=(filename,),
                            type=(
                                "primary"
                                if st.session_state.get("selected_file") == filename
                                else "secondary"
                            ),
                        )
                    with col2:
                        if st.session_state.get("selected_file") == filename:
                            retriever = create_retriever()
                            file_id = extract_id_from_filename(filename)
                            st.success("✅")
                        else:
                            st.write("")  # empty placeholder to keep alignment
                    with col3:
                        if st.button("❌", key=f"delete_{filename}"):
                            if delete_docs_by_original_id(vector_store, filename):
                                delete_file(directory, filename)
                                print(st.session_state)
                                st.success(f"deleted")
            else:
                st.info("No files found in this directory.")

        query = st.chat_input("Please ask your question")
        if query and retriever:
            relevant_docs = retriever.invoke(query, filter={"original_doc_id": file_id})

            print("relevant_docs:", relevant_docs)
            # the session state is used to store the chat history thanks to the RunnableWithMessageHistory

            model_response = get_chat_response(query, relevant_docs)
            history = st.session_state.get("chat2")
            # model_response = chain.run(input_documents=relevant_docs, question=query)
            if history:
                with st.container():
                    for msg in history.messages:
                        if isinstance(msg, HumanMessage):
                            st.chat_message("user").write(msg.content)
                        elif isinstance(msg, AIMessage):
                            st.chat_message("assistant").write(msg.content)
        else:
            st.warning("Please select a file and ask your question.")
    except Exception as e:
        # delete_file(directory, filename)
        st.error(f"Error: {e}")


if __name__ == "__main__":
    main()
