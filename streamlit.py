import streamlit as st
from main import *


if __name__ == "__main__":
     st.set_page_config(page_title="AI Assistant",
                              page_icon='🤖',
                              layout='centered')

     st.markdown("<h3 style='text-align: center;'>🤖 WWR Website AI Assistance</h3>", unsafe_allow_html=True)

     # Creating Session State Variable
     if 'HuggingFace_API_Key' not in st.session_state:
          st.session_state['HuggingFace_API_Key'] =''
     if 'DB' not in st.session_state:
          st.session_state['DB'] =''


     #********SIDE BAR*******
     with st.sidebar:
          st.sidebar.title("🗝️")
          st.session_state['HuggingFace_API_Key']= st.text_input("What's your HuggingFace API key?",type="password")
          load_button = st.button("Load", key="load_button")

     if load_button:
          #Proceed only if API keys are provided
          if st.session_state['HuggingFace_API_Key'] !="":

               #Fetch data from site
               site_data= get_website_data("https://weworkremotely.com/sitemap.xml")
               st.toast("Data pull done...", icon='😍')

               #Split data into chunks
               chunks_data=split_data(site_data)
               st.toast("Spliting data done...", icon='🔥')

               #Creating embeddings instance
               embeddings=create_embeddings()
               st.toast("Embeddings instance creation done...",icon='🤖')

               #Push data to Chroma
               st.session_state['DB'] = push_to_chroma(embeddings,chunks_data)
               st.toast("Pushing data to Chromadb done...")

               st.sidebar.success("Data pushed to Chromadb successfully!")
          else:
               st.sidebar.error("Ooopssss!!! Please provide API key and URL.....")


     prompt = st.text_input('Enter keyword - Job title/ Company name',key="prompt")  # The box for the text prompt
     document_count = st.slider('No.Of links to return 🔗 - (0 LOW || 5 HIGH)', 0, 5, 2,step=1)

     submit = st.button("Search")

     if submit:
        #Creating embeddings instance
          embeddings=create_embeddings()
          st.toast("Embeddings instance creation done...")

          #Pull index data from Chroma
          retriever = pull_from_chroma(st.session_state['DB'], 2)
          st.toast("Chroma index retrieval done...")

          #Fetch relavant documents from Chroma
          relavant_docs = get_relevant_docs(retriever, prompt)
          st.write(relavant_docs)

          #Displaying search results
          # st.success("Please find the search results :")
          #Displaying search results
          # st.write("search results list....")

     # for document in relavant_docs:

     #      st.write("👉**Result : "+ str(relavant_docs.index(document)+1)+"**")
     #      st.write("**Info**: "+document.page_content)
     #      st.write("**Link**: "+ document.metadata['source'])

