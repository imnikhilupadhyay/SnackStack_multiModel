
from __future__ import annotations

from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode

from snackstack.state import MenuSubGraphState
from snackstack.agents.menu_subagent import menu_model
from snackstack.tools.menu_tools import menu_tool

def build_menu_subgraph():
    builder = StateGraph(MenuSubGraphState)
    builder.add_node("menu_model", menu_model)
    builder.add_node("menu_tools", ToolNode([menu_tool]))
    builder.add_edge(START, "menu_model")
    builder.add_edge("menu_tools", "menu_model")
    return builder.compile()

menu_subgraph = build_menu_subgraph()