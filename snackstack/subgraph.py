
from __future__ import annotations

from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode

from snackstack.state import MenuSubGraphState, OrderSubGraphState
from snackstack.agents.menu_subagent import menu_model
from snackstack.agents.order_subagent import order_model
from snackstack.tools.menu_tools import menu_tool
from snackstack.tools.order_tools import search_order_id, search_order_email
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()

def build_menu_subgraph():
    builder = StateGraph(MenuSubGraphState)
    builder.add_node("menu_model", menu_model)
    builder.add_node("menu_tools", ToolNode([menu_tool]))
    builder.add_edge(START, "menu_model")
    builder.add_edge("menu_tools", "menu_model")
    return builder.compile(checkpointer=checkpointer)

def build_order_subgraph():
    builder = StateGraph(OrderSubGraphState)
    builder.add_node("order_model", order_model)
    builder.add_node("order_tools", ToolNode([search_order_id, search_order_email]))
    builder.add_edge(START, "order_model")
    builder.add_edge("order_tools", "order_model")
    return builder.compile(checkpointer=checkpointer)

menu_subgraph = build_menu_subgraph()
order_subgraph = build_order_subgraph()