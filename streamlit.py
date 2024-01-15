import streamlit as st
from main import get_response
from streamlit_chat import message

if __name__ == "__main__":
     st.set_page_config(page_title="Chat GPT Clone",
                              page_icon='💬',
                              layout='centered',
                               initial_sidebar_state='expanded')

     st.markdown("<h3 style='text-align: center;'>How can I assist you? </h3>", unsafe_allow_html=True)


     # initialize the state of the application. We need the conversation summary, messages b/n AI and Human and also the api key the user entered
     if 'conversation' not in st.session_state:
          st.session_state['conversation'] = None
     if 'messages' not in st.session_state:
          st.session_state['messages'] =[]
     if 'API_Key' not in st.session_state:
          st.session_state['API_Key'] =''


     # sidebarbar UI below
     # disable the btn when there are no messages
     with st.sidebar:
          st.title("😎")
          st.write("Click the button below to obtain a summary of your chat.")
          summarise_btn = st.button("Summarise the conversation", key="summarise", type="secondary", disabled = st.session_state['messages'] == [])

          if summarise_btn:
               summarise_placeholder = st.write("Below is the summary of our conversation ❤️:\n\n"+st.session_state['conversation'].memory.buffer)


     response_container = st.container()
     # Here we will have a container for user input text box
     container = st.container()


     # with container:
     #      with st.form(key='my_form', clear_on_submit=True):
               # user_input = st.text_area("Your question goes here:", key='input', height=100)
               # submit_button = st.form_submit_button(label='Send')
     prompt = st.chat_input("Enter a prompt here")
     if prompt:
          st.session_state['messages'].append(prompt)
          model_response=get_response(prompt)
          st.session_state['messages'].append(model_response)

          with response_container:
               for i in range(len(st.session_state['messages'])):
                    if (i % 2) == 0:
                         message(st.session_state['messages'][i], is_user=True, key=str(i) + '_user')
                    else:
                         message(st.session_state['messages'][i], key=str(i) + '_AI')
