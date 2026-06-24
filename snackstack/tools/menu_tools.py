from __future__ import annotations

from langchain.tools import tool
from snackstack.data.menu import ingest_menu_data
from snackstack.logger import setup_logger

logger = setup_logger("menu_tool")

vector_store = ingest_menu_data()

@tool
def menu_tool(query: str):
    """Search the SnackStack menu and return matching food items for the user query."""

    logger.debug("query=%s", query)
    
    try:
        retriever = vector_store.as_retriever(
            search_type = "similarity",
            search_kwargs = {
                "k": 2,
                "filter": {
                    "in_stock": True
                }
            },
        )

        docs = retriever.invoke(query)

        if not docs:
            return "No food item found matching your query."
        
        results = "Found the following food items in menu:\n\n"

        for i, doc in enumerate(docs):
            results += f"Food_Item {i}: \n{doc.page_content}\n\n"
        
        return results
    except Exception as e:
        logger.exception("Menu search tool failed")
        return f"Error searching food item: {e}"
