
from __future__ import annotations

from langgraph.graph import StateGraph, START, END

from snackstack.state import StackState
from snackstack.agents.orchestrator import orchestrator
from snackstack.agents.menu_agent import menu_agent
from snackstack.agents.order_agent import order_agent
from snackstack.agents.synthesizer import synthesizer
from snackstack.logger import setup_logger
from langgraph.checkpoint.memory import MemorySaver

logger = setup_logger("main graph")

checkpointer = MemorySaver()

def build_main_graph():
    builder = StateGraph(StackState)
    builder.add_node("orchestrator", orchestrator)
    builder.add_node("menu_agent", menu_agent)
    builder.add_node("order_agent", order_agent)
    builder.add_node("synthesizer", synthesizer)

    builder.add_edge(START, "orchestrator")
    builder.add_edge("synthesizer", END)

    return builder.compile(checkpointer=checkpointer)

main_graph = build_main_graph()