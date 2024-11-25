import os
from typing import Any
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from typing import List, Dict, Any
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
# from src.chains.hospital_review_chain import reviews_vector_chain
from src.chains.semantic_search_chunk_chain import content_vector_chain

from src.tools.tools import get_customer_service_infor
# from src.tools.summary_tool import cypher_summary
from llm.get_llm import get_embedding_function, get_model_function


print("✅✅call agent step")


@tool 
def explore_document(question: str) -> str:

    """
    Useful for answering questions about relevant information in user experience, when . Use the entire prompt
    as input to the tool. When the question is general and hard to find keywords from the question.
    For example, if the prompt is "help me find decore product work well for people with small spaces?", "Is HDMI can connect compatible with Macbook "

    This tool fetches relevant information from the marketplace database based on the question.
    """

    return content_vector_chain.invoke(question)


# @tool
# def get_from_database(text: str) -> List[Dict[str, Any]]:
#     """
#     Useful query information from databse for answering questions about customers, products, brands, orders,
#     customer reviews, sales statistics, and product availability. Use the entire prompt
#     as input to the tool. Or give the overview about the product.
#     Here is few example:
#     1. What are the specifications and features of [product_name]
#     2. How does [product_name] compare to other products in terms of sales?
#     3. How many products does [brand_name] have listed in our marketplace?
#     4. What are the most common complaints from customers about [brand_name]?
#     5. Which products are trending in the [category]?
#     """
#     return cypher_summary()


@tool
def get_customer_service() -> str:
    """
    Retrieve contact information for customer service.
    
    Example:
    "How can I contact customer service?"
    """
    return get_customer_service_infor()


agent_tools = [

    explore_document,
    get_customer_service,
    # get_from_database,
 
]

agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful chatbot designed to answer questions
            about customer experiences, product data, brands, customer
            review statistics, order details, shipping times, and product
            availability for stakeholders in an online marketplace.
            """
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent_llm_with_tools = get_model_function().bind_tools(agent_tools)

rag_agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | agent_prompt
    | agent_llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

rag_agent_executor = AgentExecutor(
    agent=rag_agent,
    tools=agent_tools,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True
)
