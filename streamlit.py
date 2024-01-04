import streamlit as st
from main import answer_query

if __name__ == "__main__":
	st.set_page_config(page_title="LangChain Demo", page_icon=":robot:", layout="centered")
	st.header("Simple QA App")

	def get_input():
			input_text = st.text_input("You: ", key="input")
			return input_text


	user_input= get_input()
	response = answer_query(user_input)

	submit = st.button('Generate')
	#If generate button is clicked
	if submit:
			st.subheader("Answer:")
			st.write(response)
