
from typing import Literal
from langgraph.graph import END
from langgraph.types import Command
from langchain_core.messages import SystemMessage, HumanMessage

from snackstack.state import MenuSubGraphState
from snackstack.agents.prompts import menu_prompt_template
from snackstack.config import langchain_llm
from snackstack.tools.menu_tools import menu_tool
from snackstack.logger import setup_logger

logger = setup_logger("menu_subagent")

menu_llm = langchain_llm.bind_tools([menu_tool])

def menu_model(state: MenuSubGraphState) -> Command[Literal["menu_tools", "__end__"]]:
    messages = [
        SystemMessage(content=menu_prompt_template),
        *state.get("messages", []),
        HumanMessage(content=f"""
            User query:
            {state["user_query"]}

            Task:
            {state["task_description"]}
        """)
    ]

    response = menu_llm.invoke(messages)

    

    if getattr(response, "tool_calls", None):
        logger.debug("menu_tool call initiated")
        return Command(update={"messages": [response]}, goto="menu_tools")

    return Command(update={"messages": [response]}, goto=END)
