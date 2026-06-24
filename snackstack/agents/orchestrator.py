
from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from snackstack.config import langchain_llm, langchain_embedding
from snackstack.logger import setup_logger
from snackstack.state import StackState, ClassificationResult
from langgraph.types import Command, Send, Interrupt
from typing import Literal
from snackstack.agents.prompts import orchestrator_prompt_template

logger = setup_logger("orchestrator agent")

def orchestrator(state: StackState) -> Command[Literal["menu_agent", "order_agent", "synthesizer"]]:
    user_query = state['user_query']

    orchestrator_llm = langchain_llm.with_structured_output(ClassificationResult)

    PROMPT = ChatPromptTemplate.from_template(orchestrator_prompt_template)

    try:
        manager_response = (PROMPT | orchestrator_llm).invoke(user_query)
    except Exception as e:
        logger.exception("manager_response failed - defaulting to menu_agent")
        manager_response = ClassificationResult(
            tasks=[], requires_synthesis=False,
            reasoning="Fallback: manager_response error"
        )

    logger.info(" routing=%s synthesis=%s",
                [t.agent for t in manager_response.tasks],
                manager_response.requires_synthesis
            )
    
    targets: list[Send] = []

    for task in manager_response.tasks:
        targets.append(Send(task.agent, {
            "messages": [],
            "user_query": user_query,
            "task_description": task.task_description
        }))

    if not targets:
        targets = [
            Send(
                "menu_agent",
                {
                    "messages": state["messages"],
                    "user_query": user_query,
                    "task_description": "Default fallback: answer using menu agent.",
                },
            )
        ]

    return Command(
        update={
            "tasks": [task.model_dump() for task in manager_response.tasks],
            "requires_synthesis": manager_response.requires_synthesis,
            "user_query": user_query
        },
        goto=targets,
    )