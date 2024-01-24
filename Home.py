import streamlit as st
from dotenv import load_dotenv
from utils import *
# from pages import *



# st.set_page_config(page_title="Ticket Tool", page_icon='🎫',
# layout='centered')

# st.markdown("<h3 style='text-align: center;'>🤖 JOB Website AI Assistance</h3>", unsafe_allow_html=True)

# # Creating Session State Variable
# if 'HuggingFace_API_Key' not in st.session_state:
#      st.session_state['HuggingFace_API_Key'] =''

# #********SIDE BAR*******
# with st.sidebar:
#      st.sidebar.title("🗝️")




#Creating session variables
if 'HR_tickets' not in st.session_state:
    st.session_state['HR_tickets'] =[]
if 'IT_tickets' not in st.session_state:
    st.session_state['IT_tickets'] =[]
if 'Transport_tickets' not in st.session_state:
    st.session_state['Transport_tickets'] =[]


def main():
    load_dotenv()
    st.set_page_config(page_title="Ticket Tool", page_icon='🎫')

    st.header("Automatic Ticket Classification Tool")
    st.write("Please ask your question:")
    user_input = st.text_input("🔍")

    if user_input:
        #creating embeddings instance...
        embeddings=create_embeddings()

        #Function to pull index data from Pinecone
        index=pull_from_pinecone("b115c8b2-fca0-4e6f-b0d3-07cc29935642","us-west1-gcp-free","tickets",embeddings)

        #This function will help us in fetching the top relevent documents from our vector store - Pinecone Index
        relavant_docs=get_similar_docs(index,user_input)

        #This will return the fine tuned response by LLM
        response=get_answer(relavant_docs,user_input)
        st.write(response)


        #Button to create a ticket with respective department
        button = st.button("Submit ticket?")

     #    if button:
     #        #Get Response
     #        embeddings = create_embeddings()
     #        query_result = embeddings.embed_query(user_input)

     #        #loading the ML model, so that we can use it to predit the class to which this compliant belongs to...
     #        department_value = predict(query_result)
     #        st.write("your ticket has been sumbitted to : "+department_value)

     #        #Appending the tickets to below list, so that we can view/use them later on...
     #        if department_value=="HR":
     #            st.session_state['HR_tickets'].append(user_input)
     #        elif department_value=="IT":
     #            st.session_state['IT_tickets'].append(user_input)
     #        else:
     #            st.session_state['Transport_tickets'].append(user_input)



if __name__ == '__main__':
    main()



