from langchain_core.documents import Document
from langchain.chains.question_answering import load_qa_chain
from vector_utils import add_documents_to_store
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
from config import get_llm
from langchain.chains.combine_documents import create_stuff_documents_chain

# https://python.langchain.com/api_reference/langchain/chains/langchain.chains.combine_documents.stuff.create_stuff_documents_chain.html

os.environ.pop("SSL_CERT_FILE", None)


def load_doc(file):
    if file:
        loader = PyPDFLoader(file)
    document = loader.load()
    return document


# Append id for easier retrieval and deletion
def split_doc(docs, file_id):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=384,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    doc_list = text_splitter.split_documents(docs)
    for doc in doc_list:
        if doc.metadata is None:
            doc.metadata = {}
        doc.metadata["original_doc_id"] = file_id

    return doc_list


def prepare_doc(file, original_id):
    doc = load_doc(file)
    texts = split_doc(doc, original_id)
    vector_store = add_documents_to_store(texts)
    return vector_store


# generate an id for the chat to be saved in store (session state)
def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in st.session_state:
        st.session_state[session_id] = ChatMessageHistory()
    return st.session_state[session_id]


def get_chat_response(input_user_message: str, docs: list[Document]):
    llm = get_llm()

    # Use the simple summarizing prompt structure
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant. Based on the following context, respond to the user's message.\n\nContext:\n{context}\n\nUser: {question}. Be a liitle descriptive in your answer. If the Context does not contain the answer, say 'I don't know'."
    )
    # prompt = ChatPromptTemplate.from_messages(
    #     [
    #         (
    #             "system",
    #             "You are a very helpful assistant. Answer the question truthfully. if you dont know just say 'I don't know'",
    #         ),
    #         MessagesPlaceholder(variable_name="history_messages"),
    #         ("human", "{input_user_message}"),
    #     ]
    # )

    # Create a chain for passing a list of Documents to a model.
    chain = create_stuff_documents_chain(llm, prompt)
    # Conversationchain is deprecated, so we use RunnableWithMessageHistory
    # to maintain the chat history.

    chain_with_message_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="history_messages",
    )
    result = chain_with_message_history.invoke(
        {
            "question": input_user_message,
            "context": docs,
        },
        {"configurable": {"session_id": "chat2"}},
    )

    return result


# which year was rawlings born ?
