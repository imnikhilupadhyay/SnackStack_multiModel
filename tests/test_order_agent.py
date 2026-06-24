from langchain_core.messages import HumanMessage
from langgraph.types import Command

from snackstack.subgraph import order_subgraph
from snackstack.agents.order_agent import order_agent


def print_messages(result: dict):
    print("\nMESSAGES:")
    for msg in result.get("messages", []):
        print(type(msg).__name__, "=>", getattr(msg, "content", msg))


def test_order_subgraph(query: str, resume_value: str | None = None):
    config = {
        "configurable": {
            "thread_id": f"test-order-subgraph-{abs(hash(query))}"
        }
    }

    state = {
        "messages": [],
        "user_query": query,
        "task_description": query,
    }

    result = order_subgraph.invoke(state, config=config)

    print("\n" + "=" * 80)
    print("ORDER SUBGRAPH TEST")
    print("QUERY:", query)
    print("=" * 80)

    if "__interrupt__" in result and result["__interrupt__"]:
        question = result["__interrupt__"][0].value
        print("\nINTERRUPT:")
        print(question)

        if resume_value:
            print("\nRESUME WITH:", resume_value)
            result = order_subgraph.invoke(
                Command(resume=resume_value),
                config=config,
            )

    print_messages(result)

    print("\nFINAL:")
    if result.get("messages"):
        print(result["messages"][-1].content)
    else:
        print(result)


def test_order_agent_wrapper(query: str):
    state = {
        "messages": [HumanMessage(content=query)],
        "user_query": query,
        "task_description": query,
    }

    config = {
        "configurable": {
            "thread_id": f"test-main-thread-{abs(hash(query))}"
        }
    }

    result = order_agent(state, config)

    print("\n" + "=" * 80)
    print("ORDER AGENT WRAPPER TEST")
    print("QUERY:", query)
    print("=" * 80)

    print("\nUPDATE:")
    print(result.update)

    print("\nGOTO:")
    print(result.goto)


if __name__ == "__main__":
    test_order_subgraph("Track my order ORD101")
    test_order_subgraph("Where is order number 102?")
    test_order_subgraph("Track order for priya.verma@example.com")

    # HITL inside order_subgraph
    test_order_subgraph("Where is my order?", resume_value="ORD101")

    # Wrapper test
    test_order_agent_wrapper("Track my order ORD101")
