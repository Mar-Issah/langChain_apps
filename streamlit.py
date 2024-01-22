import streamlit as st
from main import *


if __name__ == "__main__":
     st.set_page_config(page_title="AI Assistant",
                              page_icon='🤖',
                              layout='centered')

     st.markdown("<h3 style='text-align: center;'>🤖 Website AI Assistance</h3>", unsafe_allow_html=True)

     # Creating Session State Variable
     if 'HuggingFace_API_Key' not in st.session_state:
          st.session_state['HuggingFace_API_Key'] =''
     if 'Website_URL' not in st.session_state:
          st.session_state['Website_URL'] =''


     #********SIDE BAR*******
     with st.sidebar:
          # st.sidebar.title("🗝️")
          st.session_state['HuggingFace_API_Key']= st.text_input("What's your HuggingFace API key?",type="password")
          st.session_state['Website_URL']= st.text_input("What's your Website URL?")
          load_button = st.button("Load", key="load_button")

     if load_button:
          #Proceed only if API keys are provided
          if st.session_state['HuggingFace_API_Key'] !="" and st.session_state['Website_URL']!="" :

               #Fetch data from site
               site_data=get_website_data(st.session_state['Website_URL'])
               st.toast("Data pull done...", icon='😍')

               #Split data into chunks
               chunks_data=split_data(site_data)
               st.toast("Spliting data done...", icon='🔥')

               #Creating embeddings instance
               embeddings=create_embeddings()
               st.toast("Embeddings instance creation done...",icon='🤖')

               #Push data to Pinecone
               push_to_chroma(embeddings,chunks_data)
               st.write("Pushing data to Chromadb done...")

               st.sidebar.success("Data pushed to Chromadb successfully!")
          else:
               st.sidebar.error("Ooopssss!!! Please provide API key and URL.....")


     prompt = st.text_input('How can I help you my friend ❓',key="prompt")  # The box for the text prompt
document_count = st.slider('No.Of links to return 🔗 - (0 LOW || 5 HIGH)', 0, 5, 2,step=1)

submit = st.button("Search")


if submit:
        #Creating embeddings instance
     embeddings=create_embeddings()
     st.write("Embeddings instance creation done...")

     #Pull index data from Pinecone
     index=pull_from_pinecone(st.session_state['Pinecone_API_Key'],constants.PINECONE_ENVIRONMENT,constants.PINECONE_INDEX,embeddings)
     st.write("Pinecone index retrieval done...")

     #Fetch relavant documents from Pinecone index
     relavant_docs=get_similar_docs(index,prompt,document_count)
     st.write(relavant_docs)

     #Displaying search results
     st.success("Please find the search results :")
     #Displaying search results
     st.write("search results list....")
     for document in relavant_docs:

          st.write("👉**Result : "+ str(relavant_docs.index(document)+1)+"**")
          st.write("**Info**: "+document.page_content)
          st.write("**Link**: "+ document.metadata['source'])

