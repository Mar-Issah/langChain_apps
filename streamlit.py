import streamlit as st
from main import get_response, summarize_conversation
from langchain_core.messages import AIMessage, HumanMessage
from typing import Optional


def main():
    # Initialize session state for previous chat if not already set.
    # due to reruns, we need to store the previous chat in session state so it persists across interactions like btn clicks
    if "previous_chat" not in st.session_state:
        st.session_state["previous_chat"]= {}

    # Set page configurations
    st.set_page_config(
        page_title="ChatGPT Clone",
        page_icon='🤖💬',
        layout='centered',
        initial_sidebar_state='expanded'
    )

    st.markdown("<h3 style='text-align: center;'>How can I assist you?</h3>", unsafe_allow_html=True)

    # Sidebar UI
    with st.sidebar:
        st.title("📄💬➡️🔍")

    # Chat input
    prompt : str = st.chat_input("Enter a prompt here")

    if prompt:
        model_response = get_response(prompt)

        if model_response:
            st.sidebar.write("Summary of your chat.")
            # summarise_btn = st.sidebar.button("Summarise the conversation", key="summarise", type="secondary")
            st.sidebar.write(summarize_conversation(st.session_state["previous_chat"]))

          #   if summarise_btn:
          #      st.sidebar.write(summarize_conversation(st.session_state["previous_chat"]))

            with st.container():
                for msg in model_response.messages:
                    if isinstance(msg, HumanMessage):
                        st.chat_message("user").write(msg.content)
                    elif isinstance(msg, AIMessage):
                        st.chat_message("assistant").write(msg.content)

if __name__ == "__main__":
    main()
