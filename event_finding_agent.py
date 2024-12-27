import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


class EventFindingAgent:
    def __init__(self):
        self.grading_llm = ChatOpenAI(
            temperature=0, model="gpt-4-mini", streaming=True)
        self.rewrite_llm = ChatOpenAI(
            temperature=0, model="gpt-4-mini", streaming=True)
        self.response_llm = ChatOpenAI(
            temperature=0, model="gpt-4-mini", streaming=True)
        self.state = State(messages=[])
        # send input data into csv database

        return state

    def retrieve(self, state, data)

    def is_helpful(self, state):
        '''
        Determines whether retrieved infomration is helpful

        Args: 
            state: State
        Returns: 
            str: Whether the retrieved information is helpful (yes means it is relevent, no means it is not)
        '''
        print("---- DETERMINING IF HELPFUL ----")

        # define class for grading, passed as input later
        class Grade(BaseModel):
            binary_score: str = Field(
                description="Relevance score 'yes' or 'no'")

        # give llm tools to grade the information
        tooled_llm = self.grading_llm.with_structured_output(Grade)

        # Prompt:
        prompt = PromptTemplate(
            template="""You are a grader assessing relevance of a retrieved portion of data to a user question. 
            \n Here is the retrieved data: \n\n {context} \n\n
            Here is the user question: {question} \n
            If the document data indicates an anomaly or shift in system condition, grade it as relevent.\n
            Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.""",
            input_variables=["context", "question"],
        )

        # chain:
        chain = prompt | tooled_llm

        messages = state["messages"]
        last_message = messages[-1]

        question = messages[0].content
        docs = last_message.content

        scored_result = chain.invoke({"question": question, "context": docs})

        score = scored_result.binary_score

        if score == "yes":
            print("---DECISION: DOCS RELEVANT---")
            return "generate"

        else:
            print("---DECISION: DOCS NOT RELEVANT---")
            print(score)
            return "rewrite"

    def agent(self, state):
        '''
        Agent that interprets retrieved information 

        Args: 
            state: State
        Returns: 
            str:
        '''
        print("---- CALL AGENT ----")

        messages = state["messages"]
        model = ChatOpenAI(temperature=0, streaming=True, model="gpt-4o")
        model = model.bind_tools(tools)
        response = model.invoke(messages)
        # We return a list, because this will get added to the existing list
        return {"messages": [response]}

    def rewrite(self, state):
        """
        Transform the query to produce a better question.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with re-phrased question
        """

        print("---TRANSFORM QUERY---")
        messages = state["messages"]
        question = messages[0].content

        msg = [
            HumanMessage(
                content=f""" \n 
        Look at the input and try to reason about the underlying semantic intent / meaning. \n 
        Here is the initial question:
        \n ------- \n
        {question} 
        \n ------- \n
        Formulate an improved question: """,
            )
        ]

        # Grader
        model = self.llm
        response = model.invoke(msg)
        return {"messages": [response]}

    def generate(self, state):
        """
        Generate answer

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with re-phrased question
        """
        print("---GENERATE---")
        messages = state["messages"]
        question = messages[0].content
        last_message = messages[-1]

        docs = last_message.content

        # Prompt
        prompt = hub.pull("rlm/rag-prompt")

        # LLM
        llm = ChatOpenAI(model_name="gpt-4-mini",
                         temperature=0, streaming=True)

        # Post-processing
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # Chain
        rag_chain = prompt | llm | StrOutputParser()

        # Run
        response = rag_chain.invoke({"context": docs, "question": question})
        return {"messages": [response]}


if __name__ == "__main__":

    event_finder = EventFindingAgent()

    load_dotenv()

    # Define a new graph
    workflow = StateGraph(AgentState)

    # Define the nodes we will cycle between
    workflow.add_node("agent", event_finder.agent)  # agent
    retrieve = ToolNode([retriever_tool])
    workflow.add_node("retrieve", event_finder.retrieve)  # retrieval
    # Re-writing the question
    workflow.add_node("rewrite", event_finder.rewrite)
    workflow.add_node(
        "generate", generate
    )  # Generating a response after we know the documents are relevant
    # Call agent node to decide to retrieve or not
    workflow.add_edge(START, "agent")

    # Decide whether to retrieve
    workflow.add_conditional_edges(
        "agent",
        # Assess agent decision
        tools_condition,
        {
            # Translate the condition outputs to nodes in our graph
            "tools": "retrieve",
            END: END,
        },
    )

    # Edges taken after the `action` node is called.
    workflow.add_conditional_edges(
        "retrieve",
        # Assess agent decision
        grade_documents,
    )
    workflow.add_edge("generate", END)
    workflow.add_edge("rewrite", "agent")

    # Compile
    graph = workflow.compile()
