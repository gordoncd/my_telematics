# Event Finding Agent for Vehicle Performance

## Overview

This repository contains the initial implementation of an Event Finding Agent designed to analyze vehicle performance using telematics data. The agent leverages LangChain and LangGraph to query relevant features of the data and assess risk for specific cases.

## Current Progress

### Files and Directories

data

: Contains telematics data files.
- `preprocessing.ipynb`: Jupyter notebook for data preprocessing.


event_finding_agent.py

: Main implementation of the Event Finding Agent.

### 

## `event_finding_agent.py`



This file defines the [`EventFindingAgent`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fgordondoore%2FDocuments%2FGitHub%2Fmy_telematics%2Fevent_finding_agent.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A17%2C%22character%22%3A6%7D%7D%5D%2C%2243f9ae50-6036-4d13-b6f6-d475589186e6%22%5D "Go to definition") class and sets up the workflow for the agent's operation.

#### Key Components

1. **State Class**: Defines the state structure using [`TypedDict`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fgordondoore%2FDocuments%2FGitHub%2Fmy_telematics%2Fevent_finding_agent.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A3%2C%22character%22%3A30%7D%7D%5D%2C%2243f9ae50-6036-4d13-b6f6-d475589186e6%22%5D "Go to definition") and [`Annotated`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fgordondoore%2FDocuments%2FGitHub%2Fmy_telematics%2Fevent_finding_agent.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A2%2C%22character%22%3A19%7D%7D%5D%2C%2243f9ae50-6036-4d13-b6f6-d475589186e6%22%5D "Go to definition") for message handling.
2. **EventFindingAgent Class**: Initializes the agent with multiple LLMs for grading, rewriting, and responding. It also sets up a ChromaDB for storing and retrieving data.

#### Methods

- [`__init__`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fgordondoore%2FDocuments%2FGitHub%2Fmy_telematics%2Fevent_finding_agent.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A18%2C%22character%22%3A8%7D%7D%5D%2C%2243f9ae50-6036-4d13-b6f6-d475589186e6%22%5D "Go to definition"): Initializes the agent and sets up the ChromaDB.
- [`retrieve`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fgordondoore%2FDocuments%2FGitHub%2Fmy_telematics%2Fevent_finding_agent.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A31%2C%22character%22%3A8%7D%7D%5D%2C%2243f9ae50-6036-4d13-b6f6-d475589186e6%22%5D "Go to definition"): Retrieves relevant data chunks from the ChromaDB.
- [`is_helpful`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fgordondoore%2FDocuments%2FGitHub%2Fmy_telematics%2Fevent_finding_agent.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A33%2C%22character%22%3A8%7D%7D%5D%2C%2243f9ae50-6036-4d13-b6f6-d475589186e6%22%5D "Go to definition"): Determines whether the retrieved information is relevant.
- `agent`: Interprets retrieved information.
- `rewrite`: Transforms the query to produce a better question.
- `generate`: Generates an answer based on the relevant data.

#### Workflow

The workflow is defined using [`StateGraph`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fgordondoore%2FDocuments%2FGitHub%2Fmy_telematics%2Fevent_finding_agent.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A4%2C%22character%22%3A28%7D%7D%5D%2C%2243f9ae50-6036-4d13-b6f6-d475589186e6%22%5D "Go to definition") from LangGraph. It includes nodes for the agent, retrieval, rewriting, and generating responses. Conditional edges are used to determine the flow based on the agent's decisions.

### Example Usage

```python
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
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.