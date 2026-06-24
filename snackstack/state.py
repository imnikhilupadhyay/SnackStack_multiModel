
from __future__ import annotations

from typing import TypedDict, Annotated, List, Literal
from langchain_core.messages import BaseMessage, AnyMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
import operator

class AgentTask(BaseModel):
    """A single task assigned to a specialist agent."""

    agent: Literal["menu_agent", "order_agent"] = Field(
        description="Which agent handles this task"
    )
    task_description: str = Field(
        description="What the agent should do"
    )

class ClassificationResult(BaseModel):
    """Orchestrator's routing decision."""

    tasks: List[AgentTask] = Field(description="Tasks to dispatch")
    requires_synthesis: bool = Field(
        description="True when multiple agents must have their results merged"
    )
    reasoning: str = Field(description="Brief explanation of routing decision")

class StackState(TypedDict):
    """Main state"""
    user_query: str
    route: Literal["menu_agent", "order_agent"]
    menu_response: str
    order_response: str
    final_answer: str
    requires_synthesis: bool
    tasks: list[AgentTask]
    messages: Annotated[List[AnyMessage], add_messages]

class WorkerState(TypedDict):
    """Act as a input payload for the agents and their graphs"""
    messages: Annotated[List[AnyMessage], add_messages]
    user_query: str
    task_description: str

class MenuSubGraphState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    user_query: str
    task_description: str

class OrderSubGraphState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    user_query: str
    task_description: str
