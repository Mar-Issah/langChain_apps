import streamlit as st
from utils import *
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import joblib


if 'cleaned_data' not in st.session_state:
    st.session_state['cleaned_data'] =''
if 'sentences_train' not in st.session_state:
    st.session_state['sentences_train'] =''
if 'sentences_test' not in st.session_state:
    st.session_state['sentences_test'] =''
if 'labels_train' not in st.session_state:
    st.session_state['labels_train'] =''
if 'labels_test' not in st.session_state:
    st.session_state['labels_test'] =''
if 'svm_classifier' not in st.session_state:
    st.session_state['svm_classifier'] =''


st.title("Let's build our ML Model...")

# Create tabs
# steps to creating a model
tab_titles = ['Data Preprocessing', 'Model Training', 'Model Evaluation',"Save Model"]
tabs = st.tabs(tab_titles)

# Adding content to each tab

#Data Preprocessing TAB... Clean the data and remove the unwanted stuff
with tabs[0]:
    st.header('Data Preprocessing')
    st.write('Here we preprocess the data...')

    # Capture the CSV file
    data = st.file_uploader("Upload CSV file",type="csv")
    button = st.button("Load data",key="data")

    if button:
        with st.spinner('Wait for it...'):
            our_data=read_data(data)
            embeddings= create_embeddings()
            #
            st.session_state['cleaned_data'] = create_dataset_embeddings(our_data,embeddings)
        st.success('Done!')


#Model Training TAB
# Step 2, create the model by passing some data from which it can find some patterns to learn
with tabs[1]:
    st.header('Model Training')
    st.write('Here we train the model...')
    button = st.button("Train model",key="model")

    if button:
            with st.spinner('Wait for it...'):
                st.session_state['sentences_train'], st.session_state['sentences_test'], st.session_state['labels_train'], st.session_state['labels_test']=split_train_test__data(st.session_state['cleaned_data'])

                # Initialize a support vector machine, with class_weight='balanced' because
                # our training set has roughly an equal amount of positive and negative
                # sentiment sentences
                st.session_state['svm_classifier']  = make_pipeline(StandardScaler(), SVC(class_weight='balanced'))

                # fit the support vector machine
                st.session_state['svm_classifier'].fit(st.session_state['sentences_train'], st.session_state['labels_train'])
            st.success('Done!')

#Model Evaluation TAB
# test the datas accuracy. pass in some correct data and look at its repsonse
with tabs[2]:
    st.header('Model Evaluation')
    st.write('Here we evaluate the model...')
    button = st.button("Evaluate model",key="Evaluation")

    if button:
        with st.spinner('Wait for it...'):
            accuracy_score=get_score(st.session_state['svm_classifier'],st.session_state['sentences_test'],st.session_state['labels_test'])
            st.success(f"Validation accuracy is {100*accuracy_score}%!")


            st.write("A sample run:")


            #text="lack of communication regarding policy updates salary, can we please look into it?"
            text="Rude driver with scary driving"
            st.write("***Our issue*** : "+text)

            #Converting out TEXT to NUMERICAL representaion
            embeddings= create_embeddings()
            query_result = embeddings.embed_query(text)

            #Sample prediction using our trained model
            result= st.session_state['svm_classifier'].predict([query_result])
            st.write("***Department it belongs to*** : "+result[0])


        st.success('Done!')

#Save model TAB
# save and reuse the model
with tabs[3]:
    st.header('Save model')
    st.write('Here we save the model...')

    button = st.button("Save model",key="save")
    if button:

        with st.spinner('Wait for it...'):
             # save locally modelsvm.pk
             joblib.dump(st.session_state['svm_classifier'], 'modelsvm.pk1')
        st.success('Done!')