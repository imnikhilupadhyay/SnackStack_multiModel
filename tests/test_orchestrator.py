from langchain_core.messages import HumanMessage
from snackstack.state import StackState

from snackstack.agents.orchestrator import orchestrator


def test_query(query: str):
    state: StackState = {
        "user_query": query,
        "messages": [HumanMessage(content=query)],
        "tasks": [],
        "requires_synthesis": False,
        "menu_response": "",
        "order_response": "",
        "final_answer": "",
    }

    result = orchestrator(state)

    print("\n" + "=" * 80)
    print("QUERY:", query)
    print("=" * 80)

    print("\nUPDATE:")
    print(result.update)

    print("\nGOTO:")
    print(f"{result.goto}\n")


if __name__ == "__main__":
    test_query("Show me pizza options under 500")
    test_query("Where is my current order?")
    test_query("Track my order and suggest a dessert")