import streamlit as st
from main import get_script


if __name__ == "__main__":
     st.set_page_config(page_title="Video script writer",
                              page_icon='🎞️',
                              layout='centered')

     st.markdown("<h3 style='text-align: center;'>Video Script Writing Tool</h3>", unsafe_allow_html=True)


     # # Creating Session State Variable
     # if 'API_Key' not in st.session_state:
     #      st.session_state['API_Key'] =''

     prompt = st.text_input('Enter the topic of the video',key="prompt")
     video_length = st.text_input('What is the expected length of the video (in minutes)', key="video_length")
     temperature = st.slider('How creative should the script be - (0 LOW || 1 HIGH)', 0.0, 1.0, 0.2,step=0.1) # temperature

submit = st.button("Generate Script")

if submit:
     with st.container():
        search_result,title,script = get_script(prompt,video_length, temperature)
        #Let's generate the script
        st.subheader('Please find below')

        #Display Title
        st.subheader(":green[Title:]")
        st.success(title)

        #Display Video Script
        st.subheader(":green[Your Video Script:📝]")
        st.success(script)

        #Display Search Engine Result
        st.subheader("Check Out the DuckDuckGo Search:")
        with st.expander('Click to open'):
            st.info(search_result)

