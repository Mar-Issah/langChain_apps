import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

if __name__ == "__main__":
    st.set_page_config(page_title="LangChain Demo", page_icon=":robot:", layout="centered")
    st.header("Hey there!, I am your chat buddy.")

    # Create a session state with key sessionMessages
    if 'chats' not in st.session_state:
        st.session_state.chats = [SystemMessage(content="You are a very helpful AI assistant")]

    def answer_query(query):
        chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        st.session_state.chats.append(HumanMessage(content=query))
        #chat takes a list of SystemMessage, HumanMessage and retunr an output.
        assistant_answer = chat(st.session_state.chats)
        # we append the output to the list again. so the model can remember previous answer and get more context related answer
        st.session_state.chats.append(AIMessage(content=assistant_answer.content))
        return assistant_answer.content

    def get_input():
        input_text = st.text_input("You: ", key="input")
        return input_text

    user_input = get_input()

    submit = st.button('Generate')

    # If generate button is clicked
    if submit:
        response = answer_query(user_input)
        print(st.session_state)
        if response:
            st.subheader(":green[Answer:]")
            st.success(response)

