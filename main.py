import os
from langchain_openai import OpenAI
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from dotenv import load_dotenv

load_dotenv()

os.environ.get("OPENAI_API_KEY")
env = os.getenv("ENV", "prod")
enable_code_execution = env == "dev"


def query_agent(csv_file, query):
    # Parse the CSV file and create a Pandas DataFrame from its contents and use to perfrom any data analysis
    df = pd.read_csv(csv_file)

    llm = OpenAI(temperature=0)

    # Create a Pandas DataFrame agent.
    agent = create_pandas_dataframe_agent(
        llm, df, verbose=False, allow_dangerous_code=enable_code_execution
    )

    # Python REPL: A Python shell used to evaluating and executing Python commands.
    # It takes python code as input and outputs the result. The input python code can be generated from another tool in the LangChain
    return agent.run(query)
