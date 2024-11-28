from fastapi import FastAPI, HTTPException
from agents.rag_agent import chat_agent
from models.schemas import Message, ChatResponse
from utils.async_utils import async_retry1
from asyncio import TimeoutError,wait_for
import logging
from pydantic import BaseModel
from typing import Optional, List


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
app = FastAPI(
    title="Lyli",
    description="Endpoints for a asisstant system graph RAG chatbot",
)


@async_retry1(max_retries=3, delay=1)
async def invoke_agent_with_retry(message: Message, timeout: int = 30):
    """
    Retry the agent if a tool fails to run. This can help when there
    are intermittent connection issues to external APIs.
    """
    print("invoke_agent_with_retry")
    print(message)
    try:
        # Adding a timeout to ensure the query does not hang indefinitely
        response = await wait_for(chat_agent.ainvoke(
                                                    {"input": message.text},
                                                    {"configurable": {"session_id": message.session}}), timeout=timeout)
        return response
    except TimeoutError:
        logger.error(f"Query timed out after {timeout} seconds.")
        raise
    except Exception as e:
        logger.error(f"Error invoking agent: {e}")
        raise


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/docs-rag-agent", response_model=ChatResponse)
async def ask_docs_agent(message: Message) -> ChatResponse:
    try:
        # Call the agent with retry mechanism
        query_response = await invoke_agent_with_retry(message)
        
        if query_response is None:
            # Log the failure and return a default response indicating failure
            logger.error("invoke_agent_with_retry returned None after all retry attempts.")
            return ChatResponse(
                success=False,
                intermediate_steps=["No response from the agent."],
                output="Failed to get a response."
            )

        # Ensure 'intermediate_steps' exists in the response
        if "intermediate_steps" not in query_response:
            logger.error("Invalid response structure: 'intermediate_steps' key is missing.")
            query_response["intermediate_steps"] = ["No intermediate steps available."]

        # Process intermediate steps into strings if necessary
        try:
            query_response["intermediate_steps"] = [
                str(step) for step in query_response.get("intermediate_steps", [])
            ]
        except Exception as e:
            logger.error(f"Error processing 'intermediate_steps': {e}")
            query_response["intermediate_steps"] = ["Error processing intermediate steps."]

        # Construct the final response object
        query_response["intermediate_steps"] = [
        str(s) for s in query_response.get("intermediate_steps", [])]
        final_response = ChatResponse(
            success=True,
            intermediate_steps=query_response.get("intermediate_steps", []),
            output=query_response.get("output", "No output text provided.")
        )
        print("✅"*20)
        return final_response

    except Exception as e:
        # Catch unexpected errors, log them, and return a failure response
        logger.error(f"Unexpected error in ask_market_agent: {e}")
        return ChatResponse(
            success=False,
            intermediate_steps=["An unexpected error occurred."],
            output=str(e)
        )