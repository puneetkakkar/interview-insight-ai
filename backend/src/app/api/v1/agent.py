"""AI Agent API endpoints for FRAI Boilerplate.

This module provides endpoints for:
- Invoking AI agents
- Getting agent information
"""

from typing import Dict, Any
from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException, status
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command
from pydantic import BaseModel, Field

from app.agents.agent import DEFAULT_AGENT, AgentGraph
from app.schemas.agent import ChatMessage, UserInput

from app.core.response import build_success_response, build_error_response
from app.ai.agents import get_agent, get_all_agent_info, invoke_agent
from app.ai.rag import query_rag, add_documents_to_rag
from app.core import logger
from app.utils import langchain_to_chat_message

router = APIRouter(prefix="/agents", tags=["agents"])


# class AgentQueryRequest(BaseModel):
#     """Request model for agent queries."""    

#     query: str = Field(
#         ..., description="The query to send to the agent", min_length=1, max_length=1000
#     )


# class RAGQueryRequest(BaseModel):
#     """Request model for RAG queries."""

#     question: str = Field(
#         ...,
#         description="The question to ask the RAG system",
#         min_length=1,
#         max_length=1000,
#     )
#     k: int = Field(
#         default=3, description="Number of documents to retrieve", ge=1, le=10
#     )


# class DocumentAddRequest(BaseModel):
#     """Request model for adding documents to RAG."""

#     documents: list[str] = Field(
#         ..., description="List of documents to add", min_items=1
#     )
#     metadata: list[Dict[str, Any]] = Field(
#         default=None, description="Optional metadata for documents"
#     )


@router.get("/")
async def list_agents() -> Dict[str, Any]:
    """Get information about all available agents."""
    try:
        agents_info = get_all_agent_info()
        return build_success_response(
            data=agents_info, message="Available agents retrieved successfully"
        )
    except Exception as e:
        return build_error_response(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Failed to retrieve agent information",
            details=str(e),
        )


# @router.post("/{agent_name}/invoke")
# async def invoke_agent_endpoint(
#     agent_name: str,
#     request: AgentQueryRequest
# ) -> Dict[str, Any]:
#     """Invoke a specific agent with a query."""
#     try:
#         # Validate agent exists
#         if agent_name not in [agent["name"] for agent in get_all_agent_info()]:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Agent '{agent_name}' not found"
#             )

#         # Invoke the agent
#         response = await invoke_agent(agent_name, request.query)

#         return build_success_response(
#             data={
#                 "agent": agent_name,
#                 "query": request.query,
#                 "response": response
#             },
#             message="Agent invoked successfully"
#         )

#     except HTTPException:
#         raise
#     except Exception as e:
#         return build_error_response(
#             code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             message="Failed to invoke agent",
#             details=str(e)
#         )


async def _handle_input(
    user_input: UserInput, agent: AgentGraph
) -> tuple[dict[str, Any], UUID]:
    """
    Parse user input and handle any required interrupt resumption.
    Returns kwargs for agent invocation and the run_id.
    """
    run_id = uuid4()
    thread_id = user_input.thread_id or str(uuid4())
    user_id = user_input.user_id or str(uuid4())

    configurable = {
        "thread_id": thread_id,
        "model": user_input.model,
        "user_id": user_id,
    }

    if user_input.agent_config:
        if overlap := configurable.keys() & user_input.agent_config.keys():
            raise HTTPException(
                status_code=422,
                detail=f"agent_config contains reserved keys: {overlap}",
            )
        configurable.update(user_input.agent_config)

    config = RunnableConfig(
        configurable=configurable,
        run_id=run_id,
    )

    # Check for interrupts that need to be resumed
    state = await agent.aget_state(config=config)
    interrupted_tasks = [
        task for task in state.tasks if hasattr(task, "interrupts") and task.interrupts
    ]

    input: Command | dict[str, Any]
    if interrupted_tasks:
        # assume user input is response to resume agent execution from interrupt
        input = Command(resume=user_input.message)
    else:
        input = {"messages": [HumanMessage(content=user_input.message)]}

    kwargs = {
        "input": input,
        "config": config,
    }

    return kwargs, run_id


@router.post("/{agent_id}/invoke")
@router.post("/invoke")
async def invoke(user_input: UserInput, agent_id: str = DEFAULT_AGENT) -> ChatMessage:
    """
    Invoke an agent with user input to retrieve a final response.

    If agent_id is not provided, the default agent will be used.
    Use thread_id to persist and continue a multi-turn conversation. run_id kwarg
    is also attached to messages for recording feedback.
    Use user_id to persist and continue a conversation across multiple threads.
    """
    agent: AgentGraph = get_agent(agent_id)
    kwargs, run_id = await _handle_input(user_input, agent)

    try:
        response_events: list[tuple[str, Any]] = await agent.ainvoke(**kwargs, stream_mode=["updates", "values"])  # type: ignore # fmt: skip
        response_type, response = response_events[-1]
        if response_type == "values":
            # Normal response, the agent completed successfully
            output = langchain_to_chat_message(response["messages"][-1])
        elif response_type == "updates" and "__interrupt__" in response:
            # The last thing to occur was an interrupt
            # Return the value of the first interrupt as an AIMessage
            output = langchain_to_chat_message(
                AIMessage(content=response["__interrupt__"][0].value)
            )
        else:
            raise ValueError(f"Unexpected response type: {response_type}")

        output.run_id = str(run_id)
        return output
    except Exception as e:
        logger.error(f"An exception occurred: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error")


# @router.post("/rag/query")
# async def rag_query(request: RAGQueryRequest) -> Dict[str, Any]:
#     """Query the RAG system."""
#     try:
#         response = await query_rag(request.question, request.k)

#         return build_success_response(
#             data={
#                 "question": request.question,
#                 "response": response,
#                 "k": request.k
#             },
#             message="RAG query processed successfully"
#         )

#     except Exception as e:
#         return build_error_response(
#             code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             message="Failed to process RAG query",
#             details=str(e)
#         )


# @router.post("/rag/documents")
# async def add_documents(request: DocumentAddRequest) -> Dict[str, Any]:
#     """Add documents to the RAG system."""
#     try:
#         await add_documents_to_rag(request.documents, request.metadata)

#         return build_success_response(
#             data={
#                 "documents_added": len(request.documents),
#                 "metadata_provided": request.metadata is not None
#             },
#             message="Documents added to RAG system successfully"
#         )

#     except Exception as e:
#         return build_error_response(
#             code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             message="Failed to add documents to RAG system",
#             details=str(e)
#         )


# @router.get("/rag/info")
# async def rag_info() -> Dict[str, Any]:
#     """Get information about the RAG system."""
#     try:
#         from ...ai.rag import get_rag_pipeline
#         pipeline = get_rag_pipeline()
#         doc_count = await pipeline.get_document_count()

#         return build_success_response(
#             data={
#                 "document_count": doc_count,
#                 "vector_store_type": "ChromaDB (in-memory)",
#                 "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"
#             },
#             message="RAG system information retrieved successfully"
#         )

#     except Exception as e:
#         return build_error_response(
#             code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             message="Failed to retrieve RAG information",
#             details=str(e)
#         )
