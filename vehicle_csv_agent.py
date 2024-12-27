import os
from dotenv import load_dotenv
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI
import pandas as pd
from langchain.agents.agent_types import AgentType
from langchain.prompts import PromptTemplate


class CSVAgent:
    def __init__(self, csv_path: str = "data/v2_clean.csv"):
        load_dotenv()
        self.llm = ChatOpenAI(temperature=0, verbose=True, model='gpt-4o')

        # Define custom prompt templates
        self.system_template = PromptTemplate(
            template="You are a telematics data monitoring professional.  You search for when vehicles in a fleet may be prone to breakdown.  You are given data and then will be asked to perform some action pertaining to telematics monitoring with it. \n{data}\n"
        )
        self.user_template = PromptTemplate(
            template="{query}"
        )

        self.agent = create_csv_agent(
            self.llm, csv_path, verbose=True, agent_type=AgentType.OPENAI_FUNCTIONS, allow_dangerous_code=True)

    def run(self, query: str) -> str:
        print(f"Query: {query}")
        response = self.agent.invoke(query)
        print(f"Response: {response}")
        return response


if __name__ == "__main__":
    agent = CSVAgent(csv_path="data/v2_clean.csv")
    print(agent.run(
        "What conditions cause the most stress on the engine? Find and describe how these conditions work together. Can you consider evidence in the data with specific mechanisms inside engines. Make sure to investigate specific statistiscs about engine behavior in this data and when the system could be most stressed based on the analyzed conditions. Report the most important features to determining the idea of interest. Only provide the features of interest and nothing else")['output'])
