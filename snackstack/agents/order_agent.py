
from __future__ import annotations

from typing import Literal
from langgraph.types import Command, interrupt

from snackstack.state import WorkerState
from snackstack.subgraph import order_subgraph
from snackstack.logger import setup_logger
from uuid import uuid4
from langchain_core.messages import AIMessage

logger = setup_logger("order_agent")

def order_agent(state: WorkerState, config) -> Command[Literal["synthesizer"]]:
    user_query = state["user_query"]
    task_description = state.get("task_description", user_query)

    parent_thread_id = config["configurable"]["thread_id"]

    logger.info("Invoking subgraph with '%s'", task_description)

    subgraph_config = {
        "configurable": {
            "thread_id": f"{parent_thread_id}:order_subgraph:{uuid4().hex}"
        }
    }

    result = order_subgraph.invoke({
        "messages": [],
        "user_query": task_description,
        "task_description": AIMessage(task_description),
    }, config=subgraph_config)

    if "__interrupt__" in result and result["__interrupt__"]:
        question = result["__interrupt__"][0].value

        user_answer = interrupt(question)

        result = order_subgraph.invoke(
            Command(resume=user_answer),
            config=subgraph_config,
        )

    final_answer = result["messages"][-1].content

    logger.info(f"order_response: {final_answer[:120]}")

    return Command(
        update={"order_response": final_answer},
        goto="synthesizer",
    )
