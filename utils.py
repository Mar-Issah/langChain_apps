from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.llms import OpenAI
# import pinecone
from langchain.vectorstores import Pinecone as pc
import pandas as pd
from sklearn.model_selection import train_test_split
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import joblib
import os
# since there have been changes import Pinecone directly from Pinecone and alias above as pc from lc
from pinecone import Pinecone


pinecone_api_key=os.environ["PINECONE_API_KEY"]


#**********Functions to load data to PINECONE************
#Read PDF data
def read_pdf_data(pdf_file):
    pdf_page = PdfReader(pdf_file)
    text = ""
    for page in pdf_page.pages:
        text += page.extract_text()
    return text

#Split data into chunks
def split_data(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    docs = text_splitter.split_text(text)
    docs_chunks =text_splitter.create_documents(docs)
    return docs_chunks

#Create embeddings instance
def create_embeddings():
    #embeddings = OpenAIEmbeddings()
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings

#Function to push data to Pinecone
def push_to_pinecone(pinecone_index_name, embeddings, docs):
    # pineone.init below is no longer supported
    # pinecone.init(
    # api_key=pinecone_api_key,
    # environment=pinecone_environment
    # )
    Pinecone(api_key=pinecone_api_key)
    index_name = pinecone_index_name
    index = pc.from_documents(docs, embeddings, index_name=index_name)
    return index




#*********Functions for Model related tasks************
#Read dataset for model creation - retrun a df
def read_data(data):
    df = pd.read_csv(data,delimiter=',', header=None)
    return df

#Create embeddings instance - fxn above
#Generating embeddings for our input dataset
def create_dataset_embeddings(df, embeddings):
    df[2] = df[0].apply(lambda x: embeddings.embed_query(x))
    return df

#Splitting the data into train & test
def split_train_test__data(df_sample):
    # Split into training and testing sets
    sentences_train, sentences_test, labels_train, labels_test = train_test_split(
    list(df_sample[2]), list(df_sample[1]), test_size=0.25, random_state=0)
    print(len(sentences_train))
    return sentences_train, sentences_test, labels_train, labels_test

#Get the accuracy score on test data
def get_score(svm_classifier,sentences_test,labels_test):
    score = svm_classifier.score(sentences_test, labels_test)
    return score



#*******UTILs FOR USERS****************
#Function to pull index data from Pinecone...
def pull_from_pinecone(pinecone_index_name,embeddings):
    # pinecone.init(
    # api_key=pinecone_apikey,
    # environment=pinecone_environment
    # )
    Pinecone(api_key=pinecone_api_key)
    index_name = pinecone_index_name
    index = pc.from_existing_index(index_name, embeddings)
    return index

# def create_embeddings():
#     embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
#     return embeddings

#This function will help us in fetching the top relevent documents from our vector store - Pinecone Index
def get_similar_docs(index, query,k=2):
    similar_docs = index.similarity_search(query, k=k)
    return similar_docs

def get_answer(docs,user_input):
    chain = load_qa_chain(OpenAI(), chain_type="stuff")
    with get_openai_callback() as cb:
        response = chain.run(input_documents=docs, question=user_input)
    return response


def predict(query_result):
    Fitmodel = joblib.load('modelsvm.pk1')
    result=Fitmodel.predict([query_result])
    return result[0]