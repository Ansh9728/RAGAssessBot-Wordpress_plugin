from .vectordb import get_retriver_tool
from typing import Annotated, Literal, Sequence
from typing_extensions import TypedDict

from langchain import hub
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langgraph.prebuilt import tools_condition
from langchain_groq import ChatGroq
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
import requests
from .vectordb import get_retriver_tool
from fastapi import HTTPException

class AgentState(TypedDict):
  messages: Annotated[Sequence[BaseMessage], add_messages]

# tools = requests.get("http://127.0.0.1:8000/tools").json.get('tools')

def get_documents_from_wordpress():
    try:
        url = "http://localhost/RagAssessBot/wp-json/store_chunk_docs/v1/get-documents"
        response = requests.get(url)
        if response.status_code==200:
            documents = response.json()
            return documents
        else:
            return response.status_code

    except HTTPException as e:
        raise(str(e))


# Check for documents
docs = get_documents_from_wordpress()
if docs:
    print(docs)
    tools = get_retriver_tool(docs)


def grade_documents(state) -> Literal['generate', "rewrite"]:

    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (messages): The current state

    Returns:
        str: A decision for whether the documents are relevant or not
    """
    print("---CHECK RELEVANCE---")


    # Data Model
    class grade(BaseModel):
      """Binary score for relevence check"""

      binary_score: str = Field(description="Relevance score 'yes' or 'no'")

    model = ChatGroq(
        temperature=0,
        model="llama3-groq-70b-8192-tool-use-preview",
        api_key = "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",
        streaming=True
    )

    # LLM with tool validation structure output method is used to validate the schema of the output
    llm_with_tool = model.with_structured_output(grade)

    prompt = PromptTemplate(
        template="""You are a grader assessing relevance of a retrieved document to a user question. \n
        Here is the retrieved document: \n\n {context} \n\n
        Here is the user question: {question} \n
        If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.""",
        input_variables=["context", "question"],
    )

    chain = prompt | llm_with_tool

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


# Agent Node
def agent(state):
    """
    Invokes the agent model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply end.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with the agent response appended to messages
    """
    print("---CALL AGENT---")

    messages = state['messages']

    model = ChatGroq(
        temperature=0,
        model="llama3-70b-8192",
        api_key = "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",
        streaming=True
    )

    model = model.bind_tools(tools)
    response = model.invoke(messages)

    # We return a list, because this will get added to the existing list
    return {"messages": [response]}



def rewrite(state):
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


    model = ChatGroq(
        temperature=0,
        model="llama3-70b-8192",
        api_key = "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",
        streaming=True
    )

    response = model.invoke(msg)
    return {"messages": [response]}



def generate(state):
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
    llm = ChatGroq(
        temperature=0,
        model="llama3-70b-8192",
        api_key = "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",
        streaming=True
    )

    # Post-processing
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Chain
    rag_chain = prompt | llm | StrOutputParser()

    # Run
    response = rag_chain.invoke({"context": docs, "question": question})
    return {"messages": [response]}

# print("*" * 20 + "Prompt[rlm/rag-prompt]" + "*" * 20)
# prompt = hub.pull("rlm/rag-prompt").pretty_print()


# Define a New Graph
workflow = StateGraph(AgentState)

# Define the Node

workflow.add_node("agent", agent)  # agent
retrieve = ToolNode([tools])
workflow.add_node("retrieve", retrieve)  # retrieval
workflow.add_node("rewrite", rewrite)  # Re-writing the question
workflow.add_node(
    "generate", generate
)  # Generating a response after we know the documents are relevant
# Call agent node to decide to retrieve or not
workflow.add_edge(START, "agent")


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


def chatbot(user_prompt):
    print("Welcome to the chatbot! Type 'exit' to end the conversation.")

    final_response = []

    inputs = {
        "messages": [
            ("user", user_prompt),
        ]
    }

    for output in graph.stream(inputs):

        if 'generate' in output:
        # Print the generate message
            final_response.append(output['generate']['messages'][0])
    print(final_response)
    return final_response[0]