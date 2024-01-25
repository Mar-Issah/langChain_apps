import streamlit as st
from main import answer_query
import time

if __name__ == "__main__":
	st.set_page_config(page_title="LangChain Demo", page_icon=":robot:", layout="centered")
	st.header("Simple QA App")

	def get_input():
			input_text = st.text_input("You: ", key="input", placeholder="Hi there"!)
			return input_text

	user_input= get_input()
	response = answer_query(user_input)

	submit = st.button('Generate')
	#If generate button is clicked
	if submit:
			st.spinner('Fetching answer...')
			time.sleep(2)
			if response:
				st.subheader(":green[Answer:]")
				st.success(response)
