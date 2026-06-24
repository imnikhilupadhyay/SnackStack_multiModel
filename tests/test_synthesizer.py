from snackstack.agents.synthesizer import synthesizer


def run_test(name: str, state: dict):
    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)

    result = synthesizer(state)

    print("FINAL ANSWER:")
    print(result.get("final_answer"))

    print("\nMESSAGES:")
    print(result.get("messages"))


if __name__ == "__main__":
    base_state = {
        "user_query": "test query",
        "messages": [],
        "tasks": [],
        "requires_synthesis": False,
        "menu_response": "",
        "order_response": "",
        "final_answer": "",
    }

    run_test(
        "No agent response",
        {
            **base_state,
        },
    )

    run_test(
        "Only menu response",
        {
            **base_state,
            "menu_response": "Paneer Tikka is available for ₹450.",
        },
    )

    run_test(
        "Only order response",
        {
            **base_state,
            "order_response": "Your order ORD101 is out for delivery.",
        },
    )

    run_test(
        "Both responses, synthesis required",
        {
            **base_state,
            "user_query": "Track my order and suggest a dessert",
            "menu_response": "Chocolate Brownie is available for ₹220.",
            "order_response": "Your order ORD101 is out for delivery.",
            "requires_synthesis": True,
        },
    )