from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, SerializeAsAny
from .language_models import AllModelEnum, AnthropicModelName, OpenAIModelName


class TranscriptInput(BaseModel):
    """Input schema for transcript analysis."""
    
    transcript_text: str = Field(
        description="Raw interview transcript text with timestamps",
        examples=[
            "00:00:10 - Hi, can you introduce yourself?\n00:00:15 - Sure, I'm John Doe, a software engineer..."
        ]
    )
    
    model: SerializeAsAny[AllModelEnum] | None = Field(
        title="Model",
        description="LLM Model to use for transcript analysis.",
        default=AnthropicModelName.HAIKU_35,
        examples=[OpenAIModelName.GPT_4O_MINI, AnthropicModelName.HAIKU_35],
    )
    
    thread_id: str | None = Field(
        description="Thread ID to persist and continue analysis context.",
        default=None,
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"],
    )
    
    user_id: str | None = Field(
        description="User ID to persist analysis across sessions.",
        default=None,
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"],
    )
    
    custom_categories: List[str] | None = Field(
        description="Custom categories for content classification",
        default=None,
        examples=[["technical_discussion", "behavioral_questions", "company_culture"]]
    )


class TimelineEntry(BaseModel):
    """Individual timeline entry with timestamp and categorized content."""
    
    timestamp: str | None = Field(
        description="Timestamp in MM:SS or HH:MM:SS format",
        examples=["00:02:30", "1:15:45"]
    )
    
    category: str = Field(
        description="Content category classification",
        examples=["introduction", "problem_description", "solution_discussion", "coding", "testing", "questions", "conclusion"]
    )
    
    content: str = Field(
        description="Content of the timeline entry",
        examples=["Candidate introduces their background in full-stack development"]
    )
    
    confidence_score: float | None = Field(
        description="Confidence score for the categorization (0.0 to 1.0)",
        ge=0.0,
        le=1.0,
        default=None,
        examples=[0.85]
    )


class EntityExtraction(BaseModel):
    """Extracted entities from the transcript."""
    
    people: List[str] = Field(
        description="Names of people mentioned in the transcript",
        default=[],
        examples=[["John Doe", "Sarah Smith", "Mike Johnson"]]
    )
    
    companies: List[str] = Field(
        description="Company names mentioned in the transcript", 
        default=[],
        examples=[["Google", "Microsoft", "TechCorp"]]
    )
    
    technologies: List[str] = Field(
        description="Technologies, programming languages, and tools mentioned",
        default=[],
        examples=[["Python", "React", "Docker", "PostgreSQL"]]
    )
    
    locations: List[str] = Field(
        description="Locations mentioned in the transcript",
        default=[],
        examples=[["San Francisco", "New York", "Remote"]]
    )


class HighlightsLowlights(BaseModel):
    """Highlights and lowlights extracted from the transcript."""
    
    highlights: List[str] = Field(
        description="Positive moments and achievements from the interview",
        default=[],
        examples=[[
            "Candidate provided an excellent solution to the algorithm problem",
            "Great communication skills demonstrated throughout the discussion"
        ]]
    )
    
    lowlights: List[str] = Field(
        description="Areas for improvement or concerning moments",
        default=[],
        examples=[[
            "Struggled with the time complexity analysis",
            "Needed multiple hints to arrive at the solution"
        ]]
    )


class TranscriptSummary(BaseModel):
    """Complete transcript analysis output."""
    
    entities: EntityExtraction = Field(
        description="Extracted entities from the transcript"
    )
    
    sentiment_analysis: HighlightsLowlights = Field(
        description="Highlights and lowlights analysis"
    )
    
    timeline: List[TimelineEntry] = Field(
        description="Chronological timeline of interview events",
        examples=[[
            {
                "timestamp": "00:00:10",
                "category": "introduction", 
                "content": "Candidate introduces themselves and their background",
                "confidence_score": 0.9
            },
            {
                "timestamp": "00:02:15",
                "category": "problem_description",
                "content": "Discussion of the technical coding challenge",
                "confidence_score": 0.85
            }
        ]]
    )
    
    total_duration: str | None = Field(
        description="Total duration of the interview",
        default=None,
        examples=["45:30"]
    )
    
    key_topics: List[str] = Field(
        description="Main topics discussed during the interview",
        default=[],
        examples=[["Algorithm Design", "System Architecture", "Past Experience", "Technical Implementation"]]
    )
    
    overall_sentiment: str = Field(
        description="Overall interview sentiment",
        examples=["Positive", "Mixed", "Negative"],
        default="Mixed"
    )
    
    metadata: Dict[str, Any] = Field(
        description="Additional metadata about the analysis",
        default={},
        examples=[{
            "processed_at": "2024-01-15T10:30:00Z",
            "model_used": "claude-3-haiku-20240307",
            "confidence_threshold": 0.7
        }]
    )


class TranscriptAnalysisResponse(BaseModel):
    """Response wrapper for transcript analysis."""
    
    success: bool = Field(
        description="Whether the analysis was successful",
        default=True
    )
    
    message: str = Field(
        description="Response message",
        examples=["Transcript analyzed successfully"]
    )
    
    data: TranscriptSummary | None = Field(
        description="Analysis results",
        default=None
    )
    
    run_id: str | None = Field(
        description="Unique identifier for this analysis run",
        default=None,
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"]
    )