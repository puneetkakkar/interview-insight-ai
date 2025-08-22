from dataclasses import dataclass
from langgraph.graph import MessagesState, CompiledStateGraph, Pregel
from langgraph.managed import RemainingSteps

from app.schemas import AgentInfo
from agents.research_assistant import research_assistant

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
    )
}


def get_agent(agent_id: str) -> AgentGraph:
    return agents[agent_id].graph


def get_all_agent_info() -> list[AgentInfo]:
    return [
        AgentInfo(key=agent_id, description=agent.description)
        for agent_id, agent in agents.items()
    ]
