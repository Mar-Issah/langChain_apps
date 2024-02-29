import streamlit as st
from main import get_response
from streamlit_chat import message

def main():
    # Set page configurations
    st.set_page_config(page_title="ChatGPT Clone",
                       page_icon='🤖💬',
                       layout='centered',
                       initial_sidebar_state='expanded')

    st.markdown("<h3 style='text-align: center;'>How can I assist you? </h3>", unsafe_allow_html=True)

    # Initialize the Application state. A state to hold the conversation summary and messages between AI and Human
    if 'conversation' not in st.session_state:
        st.session_state['conversation'] = None
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # Sidebar UI
    with st.sidebar:
        st.title("📄💬➡️🔍")
     #    st.write("Click the button below to obtain a summary of your chat.")

        # Check if conversation data is available to enable the summary button
        if st.session_state['conversation'] is None:
          st.write("I can create a summary of your chat once it is available.")
        else:
            st.write("Click the button below to obtain a summary of your chat.")
            summarise_btn = st.button("Summarise the conversation", key="summarise", type="secondary")
            if summarise_btn:
                st.write("Below is the summary of our conversation ❤️:\n\n" + st.session_state['conversation'].memory.buffer)

    response_container = st.container()
    # Here we will have a container for user input text box

    prompt = st.chat_input("Enter a prompt here")
    if prompt:
        # Append the user's prompt and by the AI's response
        st.session_state['messages'].append(prompt)
        model_response = get_response(prompt)
        st.session_state['messages'].append(model_response)

        # Finally display the user message and AI message
        with response_container:
            for i in range(len(st.session_state['messages'])):
                if (i % 2) == 0:
                    message(st.session_state['messages'][i], is_user=True, key=str(i) + '_user')
                else:
                    message(st.session_state['messages'][i], key=str(i) + '_AI')

if __name__ == "__main__":
    main()
