"""AI Agent API endpoints for InterviewInsight AI.

This module provides REST API endpoints for interacting with AI agents,
including the research assistant and transcript analyzer agents.
"""

import json
from pathlib import Path
import pickle
from typing import Dict, Any
from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException, status
from langchain_core.messages import AIMessage, HumanMessage, messages_to_dict
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command
from pydantic import BaseModel, Field

from src.app.agents.agent import DEFAULT_AGENT, AgentGraph
from src.app.schemas.agent import ChatMessage, UserInput

from src.app.core.response import build_success_response, build_error_response
from src.app.agents import get_agent, get_all_agent_info
from src.app.core import logger
from src.app.utils import (
    langchain_to_chat_message,
    transform_langgraph_error_response,
)

router = APIRouter(prefix="/agent", tags=["agents"])


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
async def invoke(
    user_input: UserInput, agent_id: str = DEFAULT_AGENT
) -> Dict[str, Any]:
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
        # TODO: Uncomment this when using real LangGraph API
        response_events: list[tuple[str, Any]] = await agent.ainvoke(
            **kwargs, stream_mode=["updates", "values"]
        )
        response_type, response = response_events[-1]

        if response_type == "values":
            # Normal response, the agent completed successfully
            output = langchain_to_chat_message(response["messages"][-1])
            output.run_id = str(run_id)
            return build_success_response(
                data=output, message="Agent invoked successfully"
            )
        elif response_type == "updates" and "__interrupt__" in response:
            # The last thing to occur was an interrupt
            # Return the value of the first interrupt as an AIMessage
            output = langchain_to_chat_message(
                AIMessage(content=response["__interrupt__"][0].value)
            )
            output.run_id = str(run_id)
            return build_success_response(
                data=output,
                message="Agent processing interrupted - user input required",
            )
        else:
            raise ValueError(f"Unexpected response type: {response_type}")

    except Exception as e:
        logger.error(f"An exception occurred: {e}")
        error_details = transform_langgraph_error_response(str(e))
        return build_error_response(
            code=error_details["code"],
            message=error_details["message"],
            details=error_details["details"],
        )
