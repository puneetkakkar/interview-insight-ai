"""Transcript Analysis API endpoints for FRAI Boilerplate.

This module provides endpoints for:
- Analyzing interview transcripts
- Extracting timeline, entities, and insights
"""

import json
import os
from typing import Dict, Any
from uuid import UUID, uuid4
from fastapi import APIRouter, status
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from src.app.agents.agent import AgentGraph
from src.app.schemas.transcript import (
    TranscriptInput,
    TranscriptSummary,
    TranscriptAnalysisResponse,
)
from src.app.core.response import build_success_response, build_error_response
from src.app.agents import get_agent
from src.app.core import logger
from src.app.utils import transform_langgraph_error_response

router = APIRouter(prefix="/transcript", tags=["transcript"])

TRANSCRIPT_AGENT_ID = "transcript-analyzer"


async def _handle_transcript_input(
    transcript_input: TranscriptInput, agent: AgentGraph
) -> tuple[dict[str, Any], UUID]:
    """
    Parse transcript input and prepare for agent invocation.
    Returns kwargs for agent invocation and the run_id.
    """
    run_id = uuid4()
    thread_id = transcript_input.thread_id or str(uuid4())
    user_id = transcript_input.user_id or str(uuid4())

    configurable = {
        "thread_id": thread_id,
        "model": transcript_input.model,
        "user_id": user_id,
    }

    config = RunnableConfig(
        configurable=configurable,
        run_id=run_id,
        # Increase recursion limit for longer transcripts with many segments
        recursion_limit=100,
    )

    # Check for interrupts that need to be resumed
    state = await agent.aget_state(config=config)
    interrupted_tasks = [
        task for task in state.tasks if hasattr(task, "interrupts") and task.interrupts
    ]

    # Prepare input with transcript context
    analysis_prompt = f"""
    Please analyze the following interview transcript:

    {transcript_input.transcript_text}

    Please provide a comprehensive analysis including:
    1. Timeline with timestamps and categories
    2. Entity extraction (people, companies, technologies, locations)
    3. Sentiment analysis (highlights and lowlights)
    4. Overall assessment and key topics

    Use the available tools to process this transcript systematically.
    """

    input_data: Command | dict[str, Any]
    if interrupted_tasks:
        # Resume from interrupt
        input_data = Command(resume=analysis_prompt)
    else:
        input_data = {
            "messages": [HumanMessage(content=analysis_prompt)],
            "transcript_text": transcript_input.transcript_text,
            "custom_categories": transcript_input.custom_categories,
        }

    kwargs = {
        "input": input_data,
        "config": config,
    }

    return kwargs, run_id


def _parse_agent_response_to_summary(response_content) -> TranscriptSummary:
    """Parse agent response content into TranscriptSummary structure."""
    try:
        # Handle structured response content from LangChain/Claude
        response_text = ""

        if isinstance(response_content, list):
            # Extract text from structured response
            for item in response_content:
                if isinstance(item, dict) and item.get("type") == "text":
                    response_text += item.get("text", "")
                elif isinstance(item, str):
                    response_text += item
        elif isinstance(response_content, str):
            response_text = response_content
        else:
            response_text = str(response_content)

        # Try to extract JSON from the response text (improved parsing)
        json_str = None

        # Method 1: Look for JSON code blocks
        if "```json" in response_text:
            start_idx = response_text.find("```json") + 7
            end_idx = response_text.find("```", start_idx)
            if end_idx != -1:
                json_str = response_text[start_idx:end_idx].strip()

        # Method 2: Look for JSON without code blocks
        elif "{" in response_text and "}" in response_text:
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            json_str = response_text[start_idx:end_idx]

        # Method 3: Try to find JSON in structured content
        if not json_str and isinstance(response_content, list):
            for item in response_content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_content = item.get("text", "")
                    if "{" in text_content and "}" in text_content:
                        # Look for JSON patterns in the text
                        start_idx = text_content.find("{")
                        end_idx = text_content.rfind("}") + 1
                        potential_json = text_content[start_idx:end_idx]

                        # Validate it's actually JSON by trying to parse it
                        try:
                            test_parse = json.loads(potential_json)
                            if isinstance(test_parse, dict) and (
                                "entities" in test_parse or "timeline" in test_parse
                            ):
                                json_str = potential_json
                                break
                        except json.JSONDecodeError:
                            continue

        if json_str:
            # Parse the JSON
            parsed_data = json.loads(json_str)

            # Ensure required fields exist with defaults
            entities = parsed_data.get("entities", {})
            sentiment_analysis = parsed_data.get("sentiment_analysis", {})
            timeline = parsed_data.get("timeline", [])

            # Create the summary with proper structure
            return TranscriptSummary(
                entities={
                    "people": entities.get("people", []),
                    "companies": entities.get("companies", []),
                    "technologies": entities.get("technologies", []),
                    "locations": entities.get("locations", []),
                },
                sentiment_analysis={
                    "highlights": sentiment_analysis.get("highlights", []),
                    "lowlights": sentiment_analysis.get("lowlights", []),
                },
                timeline=[
                    {
                        "timestamp": item.get("timestamp"),
                        "category": item.get("category", "discussion"),
                        "content": str(item.get("content", "")),
                        "confidence_score": item.get("confidence_score", 0.8),
                    }
                    for item in timeline
                ],
                total_duration=parsed_data.get("total_duration"),
                key_topics=parsed_data.get("key_topics", []),
                overall_sentiment=parsed_data.get("overall_sentiment", "Mixed"),
                metadata=parsed_data.get("metadata", {"processed": True}),
            )

        # Fallback: create basic structure from text
        return TranscriptSummary(
            entities={
                "people": [],
                "companies": [],
                "technologies": [],
                "locations": [],
            },
            sentiment_analysis={"highlights": [], "lowlights": []},
            timeline=[
                {
                    "timestamp": None,
                    "category": "discussion",
                    "content": (
                        response_text[:200] + "..."
                        if len(response_text) > 200
                        else response_text
                    ),
                    "confidence_score": 0.5,
                }
            ],
            overall_sentiment="Mixed",
            key_topics=["Interview Discussion"],
            metadata={"parsed_from_text": True},
        )

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        logger.warning(f"Failed to parse agent response as JSON: {e}")
        # Return a basic summary with the raw content
        content_str = (
            str(response_content)[:500] + "..."
            if len(str(response_content)) > 500
            else str(response_content)
        )
        return TranscriptSummary(
            entities={
                "people": [],
                "companies": [],
                "technologies": [],
                "locations": [],
            },
            sentiment_analysis={"highlights": [], "lowlights": []},
            timeline=[
                {
                    "timestamp": None,
                    "category": "discussion",
                    "content": content_str,
                    "confidence_score": 0.5,
                }
            ],
            overall_sentiment="Mixed",
            key_topics=["Interview Analysis"],
            metadata={"parse_error": str(e)},
        )


@router.post("/analyze")
async def analyze_transcript(
    transcript_input: TranscriptInput,
) -> TranscriptAnalysisResponse:
    """
    Analyze an interview transcript to extract insights, timeline, and entities.

    This endpoint processes interview transcripts and returns:
    - Timeline with timestamps and categorized content
    - Entity extraction (people, companies, technologies, locations)
    - Sentiment analysis (highlights and lowlights)
    - Overall assessment and key topics
    """
    try:
        agent: AgentGraph = get_agent(TRANSCRIPT_AGENT_ID)
        kwargs, run_id = await _handle_transcript_input(transcript_input, agent)

        # Invoke the real LangGraph agent with improved error handling
        try:
            logger.info(f"Invoking transcript analyzer agent for run_id: {run_id}")
            response_events: list[tuple[str, Any]] = await agent.ainvoke(
                **kwargs, stream_mode=["updates", "values"]
            )

            if not response_events:
                logger.error("No response events received from agent")
                raise ValueError("Agent returned no response events")

            response_type, response = response_events[-1]
            logger.info(f"Agent response type: {response_type}")

        except Exception as agent_error:
            logger.error(f"Agent invocation failed: {str(agent_error)}")
            logger.error(f"Agent error type: {type(agent_error)}")
            raise ValueError(
                f"Agent processing failed: {str(agent_error)}"
            ) from agent_error

        if response_type == "values":
            # Normal response - parse the agent's analysis
            try:
                if "messages" not in response or not response["messages"]:
                    logger.error("No messages in agent response")
                    raise ValueError("Agent response missing messages")

                response_content = response["messages"][-1].content
                logger.info(f"Agent response content type: {type(response_content)}")
                logger.info(
                    f"Agent response content length: {len(str(response_content))}"
                )

                summary = _parse_agent_response_to_summary(response_content)

                # Save the actual LLM response for future testing
                if os.environ.get("ENV") == "development":
                    with open("actual_llm_response.json", "w") as f:
                        json.dump(
                            {
                                "response_content": response_content,
                                "parsed_summary": summary,
                                "run_id": str(run_id),
                            },
                            f,
                            indent=4,
                            default=str,
                        )

                    logger.info(
                        "Successfully saved LLM response to actual_llm_response.json"
                    )

            except Exception as parse_error:
                logger.error(f"Response parsing failed: {str(parse_error)}")
                raise ValueError(
                    f"Failed to parse agent response: {str(parse_error)}"
                ) from parse_error

            return TranscriptAnalysisResponse(
                success=True,
                message="Transcript analyzed successfully",
                data=summary,
                run_id=str(run_id),
            )
        elif response_type == "updates" and "__interrupt__" in response:
            # Handle interrupt case
            return TranscriptAnalysisResponse(
                success=False,
                message="Analysis interrupted - additional input required",
                data=None,
                run_id=str(run_id),
            )
        else:
            raise ValueError(f"Unexpected response type: {response_type}")

    except Exception as e:
        logger.error(f"Transcript analysis failed: {e}")
        logger.error(f"Exception type: {type(e)}")
        logger.error(f"Full traceback:", exc_info=True)

        error_details = transform_langgraph_error_response(str(e))

        # Provide more specific error messages
        error_message = error_details["message"]
        if "Agent processing failed" in str(e):
            error_message = f"LLM agent failed to process transcript: {str(e)}"
        elif "Failed to parse agent response" in str(e):
            error_message = f"Could not parse LLM response: {str(e)}"
        elif "No response events" in str(e):
            error_message = "LLM agent returned no response - possible timeout or configuration issue"

        return TranscriptAnalysisResponse(
            success=False,
            message=f"Failed to analyze transcript: {error_message}",
            data=None,
            run_id=str(run_id) if "run_id" in locals() else None,
        )


@router.get("/agents")
async def list_transcript_agents() -> Dict[str, Any]:
    """Get information about transcript analysis agents."""
    try:
        from src.app.agents import get_all_agent_info

        # Filter for transcript-related agents
        all_agents = get_all_agent_info()
        transcript_agents = [
            agent
            for agent in all_agents
            if "transcript" in agent.key.lower()
            or "transcript" in agent.description.lower()
        ]

        return build_success_response(
            data=transcript_agents,
            message="Transcript analysis agents retrieved successfully",
        )
    except Exception as e:
        return build_error_response(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Failed to retrieve transcript agent information",
            details=str(e),
        )
