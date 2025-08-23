from dataclasses import dataclass
from langgraph.graph.state import CompiledStateGraph
from langgraph.pregel import Pregel

from src.app.schemas import AgentInfo
from .research_assistant import research_assistant
from .transcript_analyzer import transcript_analyzer

DEFAULT_AGENT = "research-assistant"

AgentGraph = CompiledStateGraph | Pregel


@dataclass
class Agent:
    """Agent definition with description and graph."""

    description: str
    graph: AgentGraph


agents: dict[str, Agent] = {
    "research-assistant": Agent(
        description="A research assistant with web search and calculator.",
        graph=research_assistant,
    ),
    "transcript-analyzer": Agent(
        description="An interview transcript analyzer that extracts insights, creates timelines, and identifies key entities.",
        graph=transcript_analyzer,
    )
}


def get_agent(agent_id: str) -> AgentGraph:
    return agents[agent_id].graph


def get_all_agent_info() -> list[AgentInfo]:
    return [
        AgentInfo(key=agent_id, description=agent.description)
        for agent_id, agent in agents.items()
    ]
