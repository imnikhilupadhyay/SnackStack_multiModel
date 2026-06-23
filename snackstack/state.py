
from __future__ import annotations

from typing import TypedDict, Annotated, List, Literal
from langchain_core.messages import BaseMessage, AnyMessage
from langgraph.graph.message import add_messages

class StackState(TypedDict):
    user_query: str
    route: Literal["menu_agent", "order_agent"]
    menu_response: str
    order_response: str
    final_answer: str
    messages: Annotated[List[AnyMessage], add_messages]