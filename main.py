import os
from langchain_community.llms import OpenAI
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent


os.environ.get("OPENAI_API_KEY")

def query_agent(csv_file, query):
	# Parse the CSV file and create a Pandas DataFrame from its contents and use to perfrom any data analysis
    df = pd.read_csv(csv_file)
    print(df)

    llm = OpenAI()

	 # Create a Pandas DataFrame agent.
    agent = create_pandas_dataframe_agent(llm, df, verbose=True)

    #Python REPL: A Python shell used to evaluating and executing Python commands.
    #It takes python code as input and outputs the result. The input python code can be generated from another tool in the LangChain
    #return agent.run(query)

