
from __future__ import annotations

from snackstack.state import StackState
from snackstack.subgraph import order_subgraph
from snackstack.logger import setup_logger
from snackstack.config import langchain_llm
from snackstack.agents.prompts import synthesizer_prompt_template
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

logger = setup_logger("synthesizer")

def synthesizer(state: StackState) -> dict:
    order_response = state.get("order_response", "")
    menu_response = state.get("menu_response", "")

    user_query = state["user_query"]
    parts = ""

    if not order_response and not menu_response:
        logger.warning("Synthesizer received no agent results")
        return {"final_answer": "Sorry, I couldn't process that request. Please try again."}
    
    if order_response and menu_response and state["requires_synthesis"]:
        logger.info("Synthesizer  merging both agents responses")

        parts = f"""
            MENU_AGENT: 
            {menu_response}\n\n

            ORDER_AGENT: 
            {order_response}\n
        """.strip()

        PROMPT = ChatPromptTemplate.from_template(synthesizer_prompt_template)

        resposne = (PROMPT | langchain_llm | StrOutputParser()).invoke(
            {
                "user_query": user_query,
                "parts": parts
            }
        )

        return {
            "final_answer": resposne,
            "messages": [AIMessage(content=resposne)]
        }

    # Case: only menu agent responded
    if menu_response and not order_response:
        return {
            "final_answer": menu_response,
            "messages": [AIMessage(content=menu_response)]
        }

    # Case: only order agent responded
    if order_response and not menu_response:
        return {
            "final_answer": order_response,
            "messages": [AIMessage(content=order_response)]
        }

