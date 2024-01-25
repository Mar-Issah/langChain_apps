import streamlit as st
from main import *


if __name__ == "__main__":
     st.set_page_config(page_title="AI Assistant",
                              page_icon='🤖',
                              layout='centered')

     st.markdown("<h3 style='text-align: center;'>🤖 JOB Website AI Assistance</h3>", unsafe_allow_html=True)

     # Creating Session State Variable
     if 'HuggingFace_API_Key' not in st.session_state:
          st.session_state['HuggingFace_API_Key'] =''

     #********SIDE BAR*******
     with st.sidebar:
          st.sidebar.title("🗝️")
          st.session_state['HuggingFace_API_Key']= st.text_input("What's your HuggingFace API key?",type="password")
          load_button = st.button("Load", key="load_button")

     if load_button:
          #Proceed only if API keys are provided
          if st.session_state['HuggingFace_API_Key'] !="":
               if os.path.exists('./chroma_db'):
                    st.sidebar.success("Data pushed to Chromadb successfully!")
               else:
                    #Fetch data from site
                    site_data= get_website_data("https://jobs.apple.com/sitemap/sitemap-jobs-en-gb.xml")
                    st.toast("Data pull done...", icon='😍')

                    #Split data into chunks
                    chunks_data=split_data(site_data)
                    st.toast("Spliting data done...", icon='🔥')

                    #Creating embeddings instance
                    embeddings=create_embeddings()
                    st.toast("Embeddings instance creation done...",icon='🤖')

                    #Push data to Chroma
                    db = push_to_chroma(embeddings,chunks_data)
                    st.toast("Pushing data to Chromadb done...")
                    st.sidebar.success("Data pushed to Chromadb successfully!")
          else:
               st.sidebar.error("Ooopssss!!! Please provide API key.....")


     prompt = st.text_input('Enter keyword - e.g Job title',key="prompt")  # The box for the text prompt
     document_count = st.slider('No.Of links to return 🔗 - (0 LOW || 5 HIGH)', 0, 5, 2,step=1)

     # submit = st.button("Search")

     with st.spinner("Searching..."):
        if st.button("Search"):
          #Pull index data from Chroma
          relavant_docs = pull_from_chroma(prompt)
          st.toast("Chroma index retrieval done...")
          # st.write(relavant_docs)
     if prompt and relavant_docs:
          if not load_button:
               if st.session_state['HuggingFace_API_Key'] !="":
                    #Displaying search results
                    st.success("Please find the search results :")
                    for index in range(min(document_count, len(relavant_docs))):
                         document = relavant_docs[index]
                         st.write("👉**Result : " + str(index + 1) + "**")
                         st.write("**Info**: " +get_summary(relavant_docs[index]))
                         # st.write("**Info**: " + document.page_content)
                         st.write("**Link**: " + document.metadata['source'])
                         st.markdown("-----------------------------------------------------------------------")
               else:
                    st.sidebar.error("Ooopssss!!! Please provide API key.....")

