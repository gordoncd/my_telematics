import os
from dotenv import load_dotenv
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI
import pandas as pd
from langchain.agents.agent_types import AgentType
from langchain.prompts import PromptTemplate


class CSVAgent:
    def __init__(self,
                 csv_path: str = "data/v2_clean.csv",
                 prefix: str = "You are a telematics data monitoring professional. You are given data and then will be asked to perform some action pertaining to telematics monitoring with it the data will have the name df. Analyze the data thoroughly using data analysis practices and justify your response internally, then follow the final instructions for how you report your findings.",
                 suffix: str = "return only the five most relevant column names, please confirm that these columns exist. If there are not any, return 'no data'."):
        load_dotenv()
        self.llm = ChatOpenAI(temperature=0, verbose=True, model='gpt-4o-mini')

        # Define custom prompt templates
        self.system_template = prefix
        self.user_template = suffix
        self.agent = create_csv_agent(
            self.llm, csv_path,
            prefix=self.system_template,
            suffix=self.user_template,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            allow_dangerous_code=True)

    def run(self, query: str) -> str:
        print(f"Query: {query}")
        response = self.agent.invoke(query)
        print(f"Response: {response}")
        return response

# now we want to chain csv agents together
# we will need to create a new class that will chain the csv agents together


class MultiDocAgent:

    def __init__(self, filetype_list, path_object_list, prefix_list, suffix_list):

        load_dotenv()
        self.llm = ChatOpenAI(temperature=0, verbose=True, model='gpt-4o-mini')
        self.filetype_list = filetype_list
        self.path_list = path_object_list
        self.system_template = prefix
        self.user_tmeplate = suffix
        self.agents = []
        num_filetypes = len(filetype_list)
        num_files = len(path_object_list)
        if num_filetypes != num_files:
            raise ValueError(
                f"filetype list and path/object list should be the same length, filetype_list of length {num_files} incompatible with path/object list of length {num_filetypes}")

        for i, filetype in enumerate(filetype_list):
            if filetype == "csv":
                self.agent.append(CSVAgent(
                    csv_path=path_object_list[i]), prefix=self.system_template[i], suffix=self.user_template[i])
            elif filetype == "pdf":
                self.agents.append(PDFAgent(
                    pdf_path=path_object_list[i],  prefix=self.system_template[i], suffix=self.user_template[i]))
            elif filetype == "docx":
                self.agents.append(DocxAgent(
                    docx_path=path_object_list[i], prefix=self.system_template[i], suffix=self.user_template[i]))
            else:
                raise ValueError(
                    "Filetype not supported csv, pdf, and docx support is allowed")

        self.agent_chain = None

    def agent_chain_init(self):
        self.agent_chain = AgentChain(self.agents)


class AgentChain:
    # use langgraph to chain agents together

    def __init__(self, agents: list):
        self.agents = agents

    def run(self, query: str) -> str:
        response = query
        for agent in self.agents:  # make sure waiting for response to get updated for each step here
            response = agent.run(response)['output']
        return response


if __name__ == "__main__":
    agent = CSVAgent(csv_path="data/v2_clean.csv")
    print(agent.run(
        "What conditions cause the most stress on the engine? Find and describe how these conditions work together. Can you consider evidence in the data with specific mechanisms inside engines. Make sure to investigate specific statistiscs about engine behavior in this data and when the system could be most stressed based on the analyzed conditions. Report the five most important features to determining the idea of interest. Only provide the features of interest and nothing else")['output'])
