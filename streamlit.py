import streamlit as st
from dotenv import load_dotenv
from utils import *
import uuid

#Creating session variables
if 'unique_id' not in st.session_state:
    st.session_state['unique_id'] =''

def main():
    load_dotenv()

    st.set_page_config(page_title="Resume Screening Assistance", page_icon="📝")
    st.title("HR - Resume Screening Assistance...")
    # st.subheader("I can help you in resume screening process")

    job_description = st.text_area("Please paste the 'JOB DESCRIPTION' here...", key="desc")
    document_count = st.text_input("Enter the no.of resumes to return",key="count")
    # Upload the Resumes (pdf files)
    pdf = st.file_uploader("Upload resumes here, only PDF files allowed", type=["pdf"], accept_multiple_files=True)

    submit=st.button("Screen")

    if submit:
        with st.spinner('Wait for it...'):

            #Creating a unique ID, so that we can use to query and get only the user uploaded documents from PINECONE vector store
            st.session_state['unique_id']=uuid.uuid4().hex

            #Create a documents list out of all the user uploaded pdf files
            final_docs_list=create_docs(pdf,st.session_state['unique_id'])

            #Displaying the count of resumes that have been uploaded
            st.write("*Resumes uploaded* :"+str(len(final_docs_list)))

            #Create embeddings instance
            embeddings=create_embeddings_load_data()

            #Push data to PINECONE
            # using already created index automatic-ticket-tool
            table = push_to_lancedb(embeddings)

            #Fecth relavant documents from PINECONE
            # using already created index automatic-ticket-tool
            # relavant_docs = similar_docs_lancedb(job_description,document_count,"automatic-ticket-tool", embeddings, st.session_state['unique_id'])
            relavant_docs = similar_docs_lancedb(job_description,table,embeddings,final_docs_list)

            st.write(relavant_docs)

            #Introducing a line separator
            st.write(":heavy_minus_sign:" * 30)

            #For each item in relavant docs - we are displaying some info of it on the UI
        #     for item in range(len(relavant_docs)):
        #         st.subheader("👉 "+str(item+1))

        #         #Displaying Filepath
        #         st.write("**File** : "+relavant_docs[item][0].metadata['name'])

        #         #Introducing Expander feature
        #         with st.expander('Show me 👀'):
        #             st.info("**Match Score** : "+str(relavant_docs[item][1]))
        #             #st.write("***"+relavant_docs[item][0].page_content)

        #             #Gets the summary of the current item using 'get_summary' function that we have created which uses LLM & Langchain chain
        #             summary = get_summary(relavant_docs[item][0])
        #             st.write("**Summary** : "+summary)

        # st.success("Hope I was able to save your time❤️")


#Invoking main function
if __name__ == '__main__':
    main()
