from langchain_openai import ChatOpenAI
from langchain.memory import  ChatMessageHistory
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from langchain_core.messages import AIMessage, HumanMessage,BaseMessage
from typing import List
from config import get_llm

os.environ.get("OPENAI_API_KEY")
# os.environ.pop("SSL_CERT_FILE", None)


def summarize_conversation(messages: List[BaseMessage]) -> str:
    # A summarization prompt template
    summary_prompt = PromptTemplate.from_template("""
    Summarize the following conversation in few words between a user and an assistant:

    {conversation}

    Summary:
    """)

    # Convert message history to plain text
    conversation_text = ""
    for msg in messages:
        role = "Human" if isinstance(msg, HumanMessage) else "AI"
        conversation_text += f"{role}: {msg}\n"

    # Run it through an LLM chain
    llm =get_llm()
    chain = summary_prompt | llm
    summary = chain.invoke({"conversation":conversation_text})

    return summary.content.strip()


# generate an id for chat
def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in st.session_state:
        st.session_state[session_id] = ChatMessageHistory()
    return st.session_state[session_id]


def get_response(input_user_message: str) -> ChatMessageHistory:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a very helpful assistant."),
        MessagesPlaceholder(variable_name="history_messages"),
        ("human", "{input_user_message}"),
    ])

    chain = prompt | llm

    chain_with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input_user_message",
    history_messages_key="history_messages",
)
    chain_with_message_history.invoke(
    {"input_user_message": input_user_message},
    {"configurable": {"session_id": "chat1"}},
)
# Saving in st state to prevent lost of data due to reruns.
    st.session_state['previous_chat'] = st.session_state["chat1"]
    return  st.session_state["chat1"]

