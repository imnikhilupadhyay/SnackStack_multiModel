from typing import Literal

from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import END
from langgraph.types import Command, interrupt

from snackstack.state import OrderSubGraphState
from snackstack.agents.prompts import order_prompt_template
from snackstack.config import langchain_llm
from snackstack.tools.order_tools import search_order_email, search_order_id
from snackstack.logger import setup_logger

logger = setup_logger("order_subagent")

order_llm = langchain_llm.bind_tools([search_order_email, search_order_id])


def order_model(
    state: OrderSubGraphState,
) -> Command[Literal["order_tools", "order_model", "__end__"]]:

    messages = [
        SystemMessage(content=order_prompt_template),
        *state.get("messages", []),
        HumanMessage(
            content=f"""
                User query:
                {state["user_query"]}

                Task:
                {state["task_description"]}
            """
        ),
    ]

    response = order_llm.invoke(messages)

    if getattr(response, "tool_calls", None):
        logger.debug("order_tools call initiated")
        return Command(
            update={"messages": [response]},
            goto="order_tools",
        )

    has_tool_result = any(
        isinstance(msg, ToolMessage)
        for msg in state.get("messages", [])
    )

    if has_tool_result:
        return Command(update={"messages": [response]},goto=END)

    user_reply = interrupt(
        "Please provide your order ID or registered email address."
    )

    return Command(
        update={
            "messages": [
                response,
                HumanMessage(content=str(user_reply)),
            ]
        },
        goto="order_model",
    )