import streamlit as st
from main import get_response


if __name__ == "__main__":
     st.set_page_config(page_title="CSV analyser",
                              page_icon='🖩',
                              layout='centered')

     st.markdown("<h3 style='text-align: center;'>Let's analyse your CSV file</h3>", unsafe_allow_html=True)


     uploaded_file = st.file_uploader("Please upload your CSV file", type=["csv"])
     if uploaded_file is not None:
          try:
               # Save the file locally with the original file name and extension
               with open(uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getvalue())
                    st.toast(f"File saved as {uploaded_file.name}", icon='😍')


               # Process the file based on its extension
               with st.spinner("Processing..."):
                    if uploaded_file:

                         submit_btn = st.button("Submit", key="submit", type="secondary")

                         if submit_btn:
                              st.subheader(":green[Answer:]")
                              st.success()
                    else:
                         st.warning("Unsupported file type. Only CSV is supported.")

          except Exception as e:
               st.error(f"Error: {e}")

