import os
from dotenv import load_dotenv
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI
import pandas as pd
from langchain.agents.agent_types import AgentType
from langchain.prompts import PromptTemplate


class CSVAgent:
    def __init__(self, csv_path: str = "data/v2_clean.csv", prefix: str = "You are a telematics data monitoring professional. You are given data and then will be asked to perform some action pertaining to telematics monitoring with it the data will have the name df. Analyze the data thoroughly using data analysis practices and justify your response internally, then follow the final instructions for how you report your findings.", suffix: str = "return only the five most relevant column names, please confirm that these columns exist. If there are not any, return 'no data'."):
        load_dotenv()
        self.llm = ChatOpenAI(temperature=0, verbose=True, model='gpt-4o-mini')

        # Define custom prompt templates
        self.system_template = prefix
        self.user_template = suffix
        self.agent = create_csv_agent(
            self.llm, csv_path, prefix=self.system_template, suffix=self.user_template, verbose=True, agent_type=AgentType.OPENAI_FUNCTIONS, allow_dangerous_code=True, system_prompt=self.system_template)

    def run(self, query: str) -> str:
        print(f"Query: {query}")
        response = self.agent.invoke(query)
        print(f"Response: {response}")
        return response

# now we want to define a class that will allow us to chain the agents together
# lets use langgraph for this


if __name__ == "__main__":
    agent = CSVAgent(csv_path="data/v2_clean.csv")
    print(agent.run(
        "What conditions cause the most stress on the engine? Find and describe how these conditions work together. Can you consider evidence in the data with specific mechanisms inside engines. Make sure to investigate specific statistiscs about engine behavior in this data and when the system could be most stressed based on the analyzed conditions. Report the five most important features to determining the idea of interest. Only provide the features of interest and nothing else")['output'])
