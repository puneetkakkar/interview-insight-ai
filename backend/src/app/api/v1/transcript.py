"""Transcript Analysis API endpoints for InterviewInsight AI.

This module provides REST API endpoints for analyzing interview transcripts
using AI-powered agents for timeline extraction, entity recognition, and sentiment analysis.
"""

import json
import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
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

# Cache directory for development
CACHE_DIR = Path("src/data/llm_responses")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _generate_cache_key(
    transcript_text: str, custom_categories: Optional[list] = None
) -> str:
    """Generate a unique cache key based on transcript content and categories."""
    # Create a hash of the transcript text and categories
    content_to_hash = transcript_text
    if custom_categories:
        content_to_hash += "|" + "|".join(sorted(custom_categories))

    return hashlib.md5(content_to_hash.encode()).hexdigest()


def _get_cached_response(cache_key: str) -> Optional[Dict[str, Any]]:
    """Retrieve cached response if it exists."""
    from src.app.core.config import settings
    
    if not settings.IS_DEVELOPMENT:
        return None

    # Look for any file that starts with the cache key
    cache_files = list(CACHE_DIR.glob(f"{cache_key}_*.json"))
    if cache_files:
        # Get the most recent file
        latest_file = max(cache_files, key=lambda x: x.stat().st_mtime)
        try:
            with open(latest_file, "r") as f:
                cached_data = json.load(f)
                logger.info(
                    f"Retrieved cached response for key: {cache_key} from {latest_file.name}"
                )
                return cached_data
        except Exception as e:
            logger.warning(f"Failed to read cached response: {e}")

    return None


def _save_response_to_cache(
    cache_key: str, response_content: Any, summary: TranscriptSummary, run_id: UUID
) -> None:
    """Save LLM response to cache with timestamp and metadata."""
    from src.app.core.config import settings
    
    if not settings.IS_DEVELOPMENT:
        return

    timestamp = datetime.now().isoformat()
    filename = f"{cache_key}_{timestamp}_{run_id}.json"
    cache_file = CACHE_DIR / filename

    try:
        cache_data = {
            "cache_key": cache_key,
            "timestamp": timestamp,
            "run_id": str(run_id),
            "response_content": response_content,
            "parsed_summary": summary.dict() if hasattr(summary, "dict") else summary,
            "transcript_hash": cache_key,
        }

        with open(cache_file, "w") as f:
            json.dump(cache_data, f, indent=4, default=str)

        logger.info(f"Successfully saved LLM response to cache: {filename}")

        # Keep only the latest 10 files per cache key to avoid disk space issues
        _cleanup_old_cache_files(cache_key)

    except Exception as e:
        logger.error(f"Failed to save response to cache: {e}")


def _cleanup_old_cache_files(cache_key: str) -> None:
    """Keep only the latest 10 cache files per key to manage disk space."""
    try:
        cache_files = list(CACHE_DIR.glob(f"{cache_key}_*.json"))
        if len(cache_files) > 10:
            # Sort by modification time and keep only the latest 10
            cache_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            files_to_delete = cache_files[10:]

            for file_to_delete in files_to_delete:
                file_to_delete.unlink()
                logger.info(f"Cleaned up old cache file: {file_to_delete.name}")
    except Exception as e:
        logger.warning(f"Failed to cleanup old cache files: {e}")


def _should_use_cache(transcript_input: TranscriptInput) -> bool:
    """Determine if we should use cached response instead of making LLM call."""
    from src.app.core.config import settings
    
    if not settings.IS_DEVELOPMENT:
        return False
    
    # Check if cache is enabled via settings
    if not settings.USE_LLM_CACHE:
        return False

    return True


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
        # Generate cache key for this request
        cache_key = _generate_cache_key(
            transcript_input.transcript_text, transcript_input.custom_categories
        )

        # Check if we should use cached response
        if _should_use_cache(transcript_input):
            cached_response = _get_cached_response(cache_key)

            if cached_response:
                logger.info(
                    f"Using cached response for transcript analysis (cache key: {cache_key})"
                )
                return TranscriptAnalysisResponse(
                    success=True,
                    message="Transcript analyzed successfully (from cache)",
                    data=cached_response["parsed_summary"],
                    run_id=cached_response["run_id"],
                )

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

                # Save the actual LLM response to cache for future testing
                _save_response_to_cache(cache_key, response_content, summary, run_id)

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


@router.get("/cache/status")
async def get_cache_status() -> Dict[str, Any]:
    """Get information about the LLM response cache."""
    try:
        from src.app.core.config import settings
        
        if not settings.IS_DEVELOPMENT:
            return build_error_response(
                code=status.HTTP_403_FORBIDDEN,
                message="Cache management only available in development environment",
                details="This endpoint is restricted to development use only",
            )
        
        cache_files = list(CACHE_DIR.glob("*.json"))
        cache_stats = {
            "total_files": len(cache_files),
            "cache_directory": str(CACHE_DIR),
            "cache_enabled": settings.USE_LLM_CACHE,
            "environment": settings.ENVIRONMENT,
        }
        
        # Group files by cache key
        cache_groups = {}
        for cache_file in cache_files:
            try:
                with open(cache_file, "r") as f:
                    data = json.load(f)
                    cache_key = data.get("cache_key", "unknown")
                    if cache_key not in cache_groups:
                        cache_groups[cache_key] = []
                    cache_groups[cache_key].append({
                        "filename": cache_file.name,
                        "timestamp": data.get("timestamp"),
                        "run_id": data.get("run_id"),
                        "file_size": cache_file.stat().st_size,
                    })
            except Exception as e:
                logger.warning(f"Failed to read cache file {cache_file.name}: {e}")
        
        cache_stats["cache_groups"] = cache_groups
        cache_stats["unique_cache_keys"] = len(cache_groups)
        
        return build_success_response(
            data=cache_stats,
            message="Cache status retrieved successfully",
        )
    except Exception as e:
        return build_error_response(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Failed to retrieve cache status",
            details=str(e),
        )


@router.delete("/cache/clear")
async def clear_cache() -> Dict[str, Any]:
    """Clear all cached LLM responses."""
    try:
        from src.app.core.config import settings
        
        if not settings.IS_DEVELOPMENT:
            return build_error_response(
                code=status.HTTP_403_FORBIDDEN,
                message="Cache management only available in development environment",
                details="This endpoint is restricted to development use only",
            )
        
        cache_files = list(CACHE_DIR.glob("*.json"))
        cleared_count = 0
        
        for cache_file in cache_files:
            try:
                cache_file.unlink()
                cleared_count += 1
            except Exception as e:
                logger.warning(f"Failed to delete cache file {cache_file.name}: {e}")
        
        logger.info(f"Cleared {cleared_count} cache files")
        
        return build_success_response(
            data={"cleared_files": cleared_count},
            message=f"Cache cleared successfully - {cleared_count} files removed",
        )
    except Exception as e:
        return build_error_response(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Failed to clear cache",
            details=str(e),
        )


@router.get("/cache/responses/{cache_key}")
async def get_cached_responses(cache_key: str) -> Dict[str, Any]:
    """Get all cached responses for a specific cache key."""
    try:
        from src.app.core.config import settings
        
        if not settings.IS_DEVELOPMENT:
            return build_error_response(
                code=status.HTTP_403_FORBIDDEN,
                message="Cache management only available in development environment",
                details="This endpoint is restricted to development use only",
            )
        
        cache_files = list(CACHE_DIR.glob(f"{cache_key}_*.json"))
        responses = []
        
        for cache_file in cache_files:
            try:
                with open(cache_file, "r") as f:
                    data = json.load(f)
                    responses.append({
                        "filename": cache_file.name,
                        "timestamp": data.get("timestamp"),
                        "run_id": data.get("run_id"),
                        "parsed_summary": data.get("parsed_summary"),
                        "file_size": cache_file.stat().st_size,
                    })
            except Exception as e:
                logger.warning(f"Failed to read cache file {cache_file.name}: {e}")
        
        # Sort by timestamp (newest first)
        responses.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return build_success_response(
            data={
                "cache_key": cache_key,
                "total_responses": len(responses),
                "responses": responses,
            },
            message=f"Retrieved {len(responses)} cached responses for key: {cache_key}",
        )
    except Exception as e:
        return build_error_response(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Failed to retrieve cached responses",
            details=str(e),
        )
