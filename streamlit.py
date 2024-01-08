import streamlit as st
from main import sim_search

if __name__ == "__main__":
    st.set_page_config(page_title="LangChain Demo", page_icon=":robot:", layout="centered")
    st.subheader("Hey there!, I will find you synonyms for whatever you ask.")

    def get_input():
        input_text = st.text_input("You: ", key="input")
        return input_text

    user_input = get_input()

    submit = st.button('Find')

    # If generate button is clicked
    if submit:
        response = sim_search(user_input)
        if response:
            st.subheader(":green[Top Matches:]")
            st.success(response[0].page_content
                       + '\n\n' + response[1].page_content)


