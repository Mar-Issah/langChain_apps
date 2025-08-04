import streamlit as st
from dotenv import load_dotenv
from utils import *
from pinecone_utils import (
    create_store,
    push_to_pinecone,
    pull_from_pinecone,
    get_summary,
)

# Creating session variables
if "uploaded_files" not in st.session_state:
    st.session_state["uploaded_files"] = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = create_store()


def main():
    load_dotenv()

    st.set_page_config(page_title="Resume Screening Assistance", page_icon="📝")
    st.subheader("HR - Resume Screening Assistance...")
    # st.subheader("I can help you in resume screening process")
    try:
        job_description = st.text_area(
            "Please paste the 'JOB DESCRIPTION' here...", key="desc"
        )
        document_count = st.number_input(
            "Enter the no.of resumes to return",
            key="count",
            min_value=1,
        )
        # Upload the Resumes (pdf files)
        pdfs = st.file_uploader(
            "Upload resumes here, only PDF files allowed",
            type=["pdf"],
            accept_multiple_files=True,
        )
        # print(st.session_state["vector_store"])

        # If the user has uploaded any pdf files
        if pdfs and not st.session_state["uploaded_files"]:
            # Create a Document list out of all the user uploaded pdf files
            final_docs_list = create_docs(pdfs)

            # Push data to PINECONE
            push_docs = push_to_pinecone(final_docs_list)

            if push_docs:
                # Displaying the count of resumes that have been uploaded
                st.session_state["uploaded_files"] = [f.name for f in pdfs]

                st.toast("*Resumes uploaded* :" + str(len(final_docs_list)))
            else:
                st.error(
                    "Failed to upload resumes to Pinecone. Please remove the files and re-upload."
                )

        submit = st.button("Screen")

        if submit:
            with st.spinner("Wait for it..."):
                # # Creating a unique ID, so that we can use to query and get only the user uploaded documents from PINECONE vector store
                # unique_id = uuid.uuid4().hex
                # st.session_state["unique_id"] = unique_id
                # print(st.session_state)

                # FeTch relavant documents from PINECONE vector store
                results = pull_from_pinecone(job_description, document_count)

                st.write(":heavy_minus_sign:" * 30)
                st.success(f"Find below the {document_count} Resumes")

                # For each item in relavant docs - we are displaying some info of it on the UI
                for idx, (resume, score) in enumerate(results[: int(document_count)]):
                    st.subheader(
                        f"👉 Resume {str(idx + 1)} : {resume.metadata['name']}"
                    )
                    percentage = score * 100
                    st.badge(
                        f"Resume Score: {percentage:.2f}%",
                        icon=":material/check:",
                        color="green",
                    )
                    # st.write(resume.page_content)
                    st.write("SUMMARY", get_summary(resume))
                    # print(resume.metadata.name)

                    # Gets the summary of the current item using 'get_summary' function that we have created which uses LLM & Langchain chain
                    # summary = get_summary(relavant_docs[idx])
                    # print([relavant_docs[idx]])
                    # st.write("**Summary** : " + summary)

                st.success("Hope I was able to save your time❤️")
    except Exception as e:
        st.error(f"An error occurred: {e}")


# Invoking main function
if __name__ == "__main__":
    main()
