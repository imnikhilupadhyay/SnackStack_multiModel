from typing import Literal
from langgraph.types import Command

from snackstack.state import WorkerState
from snackstack.subgraph import menu_subgraph
from snackstack.logger import setup_logger

logger = setup_logger("menu_agent")

def menu_agent(state: WorkerState, config) -> Command[Literal["synthesizer"]]:
    user_query = state["user_query"]
    task_description = state.get("task_description", user_query)

    parent_thread_id = config["configurable"]["thread_id"]

    logger.info("Invoking subgraph")

    subgraph_config = {
        "configurable": {
            "thread_id": f"{parent_thread_id}:order_subgraph"
        }
    }

    result = menu_subgraph.invoke({
        "messages": [],
        "user_query": user_query,
        "task_description": task_description,
    }, config=subgraph_config)

    final_answer = result["messages"][-1].content

    logger.info(f"menu_response: {final_answer[:120]}")

    return Command(
        update={"menu_response": final_answer},
        goto="synthesizer",
    )
