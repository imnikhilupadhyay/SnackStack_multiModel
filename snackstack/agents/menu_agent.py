from typing import Literal
from langgraph.types import Command

from snackstack.state import WorkerState
from snackstack.graph import menu_subgraph
from snackstack.logger import setup_logger

logger = setup_logger("menu_agent")

def menu_agent(state: WorkerState) -> Command[Literal["synthesizer"]]:
    user_query = state["user_query"]
    task_description = state.get("task_description", user_query)

    logger.info("Invoking subgraph")

    result = menu_subgraph.invoke({
        "messages": [],
        "user_query": user_query,
        "task_description": task_description,
    })

    final_answer = result["messages"][-1].content

    logger.info(f"menu_response: {final_answer[:120]}")

    return Command(
        update={"menu_response": final_answer},
        goto="synthesizer",
    )
