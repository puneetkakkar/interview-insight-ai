from langchain_core.messages import (
    BaseMessage,
    AIMessage,
    HumanMessage,
    ToolMessage,
)
from typing import Any, Dict
from ..schemas.agent import ChatMessage


def convert_message_content_to_string(content: str | list[str | dict]) -> str:
    if isinstance(content, str):
        return content
    text: list[str] = []
    for content_item in content:
        if isinstance(content_item, str):
            text.append(content_item)
            continue
        if content_item["type"] == "text":
            text.append(content_item["text"])
    return "".join(text)


def langchain_to_chat_message(message: BaseMessage) -> ChatMessage:
    """Create a ChatMessage from a LangChain message."""
    match message:
        case HumanMessage():
            human_message = ChatMessage(
                type="human",
                content=convert_message_content_to_string(message.content),
            )
            return human_message
        case AIMessage():
            ai_message = ChatMessage(
                type="ai",
                content=convert_message_content_to_string(message.content),
            )
            if message.tool_calls:
                ai_message.tool_calls = message.tool_calls
            if message.response_metadata:
                ai_message.response_metadata = message.response_metadata
            return ai_message
        case ToolMessage():
            tool_message = ChatMessage(
                type="tool",
                content=convert_message_content_to_string(message.content),
                tool_call_id=message.tool_call_id,
            )
            return tool_message
        case _:
            raise ValueError(f"Unsupported message type: {message.__class__.__name__}")


def transform_langgraph_error_response(error_message: str) -> Dict[str, Any]:
    """Transform LangGraph API error response to standard error format."""
    # Parse common error patterns
    if "credit balance is too low" in error_message:
        return {
            "code": 402,  # Payment Required
            "message": "Insufficient credits to access the AI service",
            "details": "Your credit balance is too low to access the Anthropic API. Please upgrade your plan or purchase more credits."
        }
    elif "Error code: 400" in error_message:
        return {
            "code": 400,  # Bad Request
            "message": "Invalid request to AI service",
            "details": error_message
        }
    elif "Error code: 401" in error_message:
        return {
            "code": 401,  # Unauthorized
            "message": "Authentication failed with AI service",
            "details": error_message
        }
    elif "Error code: 429" in error_message:
        return {
            "code": 429,  # Too Many Requests
            "message": "Rate limit exceeded for AI service",
            "details": error_message
        }
    else:
        return {
            "code": 500,  # Internal Server Error
            "message": "Unexpected error occurred while processing request",
            "details": error_message
        }
