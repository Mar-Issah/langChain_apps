import streamlit as st
from main import query_agent


if __name__ == "__main__":
     st.set_page_config(page_title="CSV analyser",
                              page_icon='🖩',
                              layout='centered')

     st.markdown("<h3 style='text-align: center;'>Let's analyse your CSV file</h3>", unsafe_allow_html=True)

     file = st.file_uploader("Please upload your CSV file", type=["csv"])
     if file is not None:
          try:
               # Process the file based on its extension
               with st.spinner("Processing..."):
                    query_agent(file, 'eg')
                    if file:
                         query = st.text_area("Enter your query")
                         submit_btn = st.button("Generate", key="generate", type="secondary")

                         if submit_btn:
                              st.subheader(":green[Answer:]")
                              st.success()
                    else:
                         st.warning("Unsupported file type. Only CSV is supported.")

          except Exception as e:
               st.error(f"Error: {e}")

