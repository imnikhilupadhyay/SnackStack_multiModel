
from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from snackstack.logger import setup_logger
from snackstack.config import langchain_llm, langchain_embedding
from snackstack.state import WorkerState

logger = setup_logger("order_agent")

def order_agent(state: WorkerState):
    user_query = state["user_query"]

    menu_prompt_template = """
     You are an assitant who has access to the restrurant food items information.

     You task is to provide the write match to the user query only based on the menu options you have.

     
    """