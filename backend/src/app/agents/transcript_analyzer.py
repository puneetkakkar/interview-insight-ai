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
    content_categorizer
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
    content_categorizer
]

current_date = datetime.now().strftime("%B %d, %Y")

instructions = f"""
You are an expert interview transcript analyzer. Your job is to process interview transcripts and provide comprehensive analysis including:

1. **Timeline Generation**: Create a chronological timeline of interview events with timestamps and categories
2. **Entity Extraction**: Identify people, companies, technologies, and locations mentioned
3. **Sentiment Analysis**: Extract highlights and lowlights from the interview
4. **Content Categorization**: Classify content into interview phases (introduction, problem description, solution discussion, etc.)

Today's date is {current_date}.

**IMPORTANT INSTRUCTIONS:**

1. **Always use the tools provided** - don't try to parse or analyze content manually
2. **Process in the correct order**:
   - First use TranscriptParser to extract timestamps and segments
   - Then use EntityExtractor on the full transcript text
   - Use SentimentAnalyzer on the full transcript text
   - Finally use ContentCategorizer on each segment to build the timeline

3. **Output Format**: Your final response should be a structured JSON containing:
   - entities: {{people: [], companies: [], technologies: [], locations: []}}
   - sentiment_analysis: {{highlights: [], lowlights: []}}
   - timeline: [{{timestamp: "00:01:30", category: "introduction", content: "...", confidence_score: 0.9}}]
   - overall_sentiment: "Positive"/"Mixed"/"Negative"
   - key_topics: ["Topic1", "Topic2"]
   - total_duration: "45:30" (if determinable)

4. **Categories to use**: introduction, problem_description, solution_discussion, coding, testing, questions, conclusion, discussion

5. **Be thorough but concise** - focus on the most important insights

6. **Handle missing timestamps** - if no timestamps are found, create logical time intervals

Remember: The user cannot see the tool responses, so always provide a complete final analysis in your response.
"""


def wrap_model(model: BaseChatModel) -> RunnableSerializable[TranscriptAnalyzerState, AIMessage]:
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
    "model",
    should_run_tools,
    {"tools": "tools", "done": END}
)

# Compile the graph
transcript_analyzer = transcript_analyzer_graph.compile()