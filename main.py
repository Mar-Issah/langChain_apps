import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers


# https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main

def getLLMResponse(topic, sender, recipient, email_style):
	llm = CTransformers(model='models/llama-2-7b-chat.ggmlv3.q8_0.bin',   model_type='llama', config={'max_new_tokens': 256,'temperature': 0.01})

	#Template for building the PROMPT
	template = """
    Write a email with {style} style and includes topic :{email_topic}.\n\nSender: {sender}\nRecipient: {recipient}
    \n\nEmail Text:
    """

	# Creating the final PROMPT
	prompt = PromptTemplate(
    input_variables=["style","email_topic","sender","recipient"],
    template=template)

	#Generating the response using LLM
	response=llm(prompt.format(email_topic=topic,sender=sender,recipient=recipient,style=email_style))
	print(response)

	return response
