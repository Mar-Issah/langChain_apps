import streamlit as st
from main import getLLMResponse

if __name__ == "__main__":
    st.set_page_config(
        page_title="Generate Emails",
        page_icon="📧",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    st.header("Generate your Emails 📧")

    topic = st.text_area("Enter the message", height=175)

    # Creating columns for the UI - To receive inputs from user
    col1, col2, col3 = st.columns([10, 10, 5])
    with col1:
        email_sender = st.text_input("Sender Name")
    with col2:
        email_recipient = st.text_input("Recipient Name")
    with col3:
        email_style = st.selectbox(
            "Writing Style",
            ("Formal", "Informal", "Appreciating", "Not Satisfied", "Neutral"),
            index=0,
        )

    submit = st.button("Generate")

    # When 'Generate' button is clicked, execute the below code
    if submit:
        st.write(getLLMResponse(topic, email_sender, email_recipient, email_style))
