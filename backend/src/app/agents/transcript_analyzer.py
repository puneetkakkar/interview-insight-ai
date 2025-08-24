from datetime import datetime
from typing import Dict, Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.runnables import (
    RunnableConfig,
    RunnableLambda,
    RunnableSerializable,
)
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.managed import RemainingSteps
from langgraph.prebuilt import ToolNode

from src.app.core.llm import get_model
from src.app.core.config import settings
from .tools import (
    transcript_parser,
    entity_extractor,
    sentiment_analyzer,
    content_categorizer,
    timeline_consolidator,
)


class TranscriptAnalyzerState(MessagesState, total=False):
    """State for transcript analyzer agent."""

    remaining_steps: RemainingSteps
    transcript_text: str
    parsed_segments: str | None
    extracted_entities: str | None
    sentiment_analysis: str | None
    timeline: list[Dict[str, Any]]
    custom_categories: list[str] | None


# Tools available to the transcript analyzer
tools = [
    transcript_parser,
    entity_extractor,
    sentiment_analyzer,
    content_categorizer,
    timeline_consolidator,
]

current_date = datetime.now().strftime("%B %d, %Y")

instructions = f"""
You are an expert interview transcript analyzer. Your job is to process interview transcripts using the available tools.

Today's date is {current_date}.

**CRITICAL INSTRUCTIONS - FOLLOW EXACTLY:**

1. **MANDATORY TOOL USAGE** - You MUST use ALL the tools in this exact order. Never skip tools or provide direct analysis:
   
   STEP 1: Use TranscriptParser on the full transcript text
   STEP 2: Use EntityExtractor on the full transcript text  
   STEP 3: Use SentimentAnalyzer on the full transcript text
   STEP 4: For each segment from TranscriptParser, use ContentCategorizer to get its category
   STEP 5: Use TimelineConsolidator on the timeline JSON from step 4 to merge consecutive similar events
   
   **IMPORTANT**: Process the ENTIRE transcript - do not stop early. Ensure complete coverage from start to finish.
   
2. **FINAL JSON OUTPUT** - After using ALL tools, provide ONLY a JSON response with this exact structure:
   ```json
   {{
     "entities": {{
       "people": ["extracted names"],
       "companies": ["extracted companies"], 
       "technologies": ["extracted tech"],
       "locations": ["extracted locations"]
     }},
     "sentiment_analysis": {{
       "highlights": ["positive moments"],
       "lowlights": ["concerning moments"]
     }},
     "timeline": [
       {{
         "timestamp": "00:01:30",
         "category": "Introduction",
         "content": "timeline event description",
         "confidence_score": 0.9
       }}
     ],
     "overall_sentiment": "Positive",
     "key_topics": ["Topic1", "Topic2"],
     "total_duration": "45:30"
   }}
   ```

3. **NO NARRATIVE SUMMARIES** - Do not provide explanatory text, analysis, or commentary. Only use tools and provide the final JSON.

4. **JSON ONLY** - Your final response must be ONLY the JSON object above, nothing else.

REMEMBER: Use every tool, then respond with JSON only. No explanations, no summaries, just structured JSON data.
"""


def wrap_model(
    model: BaseChatModel,
) -> RunnableSerializable[TranscriptAnalyzerState, AIMessage]:
    """Wrap the model with transcript analysis instructions."""
    bound_model = model.bind_tools(tools)

    def preprocess_state(state: TranscriptAnalyzerState) -> list:
        """Preprocess state to include transcript context."""
        system_msg = SystemMessage(content=instructions)

        # Add transcript text to context if available
        if state.get("transcript_text"):
            context_msg = SystemMessage(
                content=f"TRANSCRIPT TO ANALYZE:\n\n{state['transcript_text']}\n\n"
                f"Please analyze this transcript using the available tools."
            )
            return [system_msg, context_msg] + state["messages"]

        return [system_msg] + state["messages"]

    preprocessor = RunnableLambda(preprocess_state, name="TranscriptStateModifier")
    return preprocessor | bound_model  # type: ignore[return-value]


async def acall_model(
    state: TranscriptAnalyzerState, config: RunnableConfig
) -> TranscriptAnalyzerState:
    """Call the model with transcript analysis context."""
    m = get_model(config["configurable"].get("model", settings.DEFAULT_MODEL))
    model_runnable = wrap_model(m)
    response = await model_runnable.ainvoke(state, config)

    # Handle remaining steps limit
    if state["remaining_steps"] < 2 and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="Sorry, need more steps to complete the transcript analysis.",
                )
            ]
        }

    return {"messages": [response]}


def should_run_tools(state: TranscriptAnalyzerState) -> str:
    """Determine if tools should be run based on the last message."""
    last_message = state["messages"][-1]

    if not isinstance(last_message, AIMessage):
        raise TypeError(f"Expected AIMessage, got {type(last_message)}")

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "done"


# Create the transcript analyzer graph
transcript_analyzer_graph = StateGraph(TranscriptAnalyzerState)

# Add nodes
transcript_analyzer_graph.add_node("model", acall_model)
transcript_analyzer_graph.add_node("tools", ToolNode(tools))

# Set entry point
transcript_analyzer_graph.set_entry_point("model")

# Add edges
transcript_analyzer_graph.add_edge("tools", "model")
transcript_analyzer_graph.add_conditional_edges(
    "model", should_run_tools, {"tools": "tools", "done": END}
)

# Compile the graph
transcript_analyzer = transcript_analyzer_graph.compile()
