import streamlit as st
from main import get_response

if __name__ == "__main__":
     st.set_page_config(page_title="Marketing Tool",
                              page_icon='✅',
                              layout='centered',
                              initial_sidebar_state='collapsed')
     with st.form("my_form", clear_on_submit=True):

          st.header("Hey, How can I help you?")

          form_input = st.text_area('Enter text', height=275)
          tasktype_option = st.selectbox(
               'Please select the action to be performed?',
               ('Write a sales copy', 'Create a tweet', 'Write a product description'),key=1)

          age_option= st.selectbox(
          'For which age group?',
          ('Kid', 'Adult', 'Senior Citizen'),key=2)
          numberOfWords= st.slider('Words limit', 1, 200, 25)

          submit = st.form_submit_button("Generate")

     if submit:      # If generate button is clicked
          response = get_response(form_input,age_option,tasktype_option)
          if response:
               st.subheader(":green[Response:]")
               st.success(response)
