from langchain_core.messages import HumanMessage

from snackstack.agents.menu_agent import menu_subgraph, menu_agent


def test_menu_subgraph(query: str):
    state = {
        "messages": [],
        "user_query": query,
        "task_description": query,
    }

    result = menu_subgraph.invoke(state)

    print("\n" + "=" * 80)
    print("QUERY:", query)
    print("=" * 80)

    print("\nMESSAGES:")
    for msg in result["messages"]:
        print(type(msg).__name__, "=>", getattr(msg, "content", msg))

    print("\nFINAL:")
    print(result["messages"][-1].content)


def test_menu_agent_wrapper(query: str):
    state = {
        "messages": [HumanMessage(content=query)],
        "user_query": query,
        "task_description": query,
    }

    result = menu_agent(state)

    print("\n" + "=" * 80)
    print("MENU AGENT WRAPPER TEST")
    print("=" * 80)

    print("UPDATE:")
    print(result.update)

    print("GOTO:")
    print(result.goto)


if __name__ == "__main__":
    test_menu_subgraph("Suggest spicy food under 500")
    test_menu_subgraph("Show me desserts")
    test_menu_subgraph("Hi, what can you do?")

    test_menu_agent_wrapper("Suggest spicy food under 500")