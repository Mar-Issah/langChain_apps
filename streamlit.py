import streamlit as st
from main import get_response

if __name__ == "__main__":
     st.set_page_config(page_title="Chat GPT Clone",
                              page_icon='💬',
                              layout='centered',
                               initial_sidebar_state='collapsed')

     st.subheader("How can I assist you today?")


     # initialize the state of the application. We need the conversation summary, messages b/n AI and Human and also the api key the user entered
     if 'conversation' not in st.session_state:
          st.session_state['conversation'] =None
     if 'messages' not in st.session_state:
          st.session_state['messages'] =[]
     if 'API_Key' not in st.session_state:
          st.session_state['API_Key'] =''


     # sidebarbar UI below
     with st.sidebar:
          st.title("😎")
          st.session_state['API_Key']= st.text_input("What's your API key?",type="password")
          summarise_btn = st.button("Summarise the conversation", key="summarise", type="secondary")

          if summarise_btn:
               summarise_placeholder = st.write("Below is the summary of our conversation ❤️:\n\n"+st.session_state['conversation'].memory.buffer)

     # with st.form("my_form"):

     #      st.subheader("Hey, How can I help you?")

     #      form_input = st.text_area('Enter text', height=275)
     #      tasktype_option = st.selectbox(
     #           'Please select the action to be performed?',
     #           ('Write a sales copy', 'Create a tweet', 'Write a product description'),key=1)

     #      age_option= st.selectbox(
     #      'For which age group?',
     #      ('Kid', 'Adult', 'Senior Citizen'),key=2)
     #      numberOfWords= st.slider('Words limit', 1, 200, 25)

     #      submit = st.form_submit_button("Generate")

     # if submit:      # If generate button is clicked
     #      response = get_response(form_input,age_option,tasktype_option)
     #      if response:
     #           st.subheader(":green[Response:]")
     #           st.success(response)
