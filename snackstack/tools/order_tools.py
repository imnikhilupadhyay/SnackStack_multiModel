
from __future__ import annotations

from langchain.tools import tool
from snackstack.data.menu import ingest_menu_data
from snackstack.logger import setup_logger
from snackstack.data.orders import order_data, get_order_by_id
import re

logger = setup_logger("order_tool")

ORDER_DATABASE = order_data

def normalize_order_id(order_id: str) -> str:
    value = order_id.upper().strip()
    digits = re.sub(r"\D", "", value)

    if not digits:
        return ""

    return f"ORD{digits}"

@tool
def search_order_id(order_id: str) -> dict | None:
    """Accept 'ORD101', 'ORD-101', 'ord-101', or just '101' → 'ORD101'."""
    normalized_order = normalize_order_id(order_id)

    if not normalized_order:
        return None

    order_details = get_order_by_id(normalized_order)

    if not order_details:
        return None

    return {
        "order_id": normalized_order,
        **order_details
    }

@tool
def search_order_email(email: str) -> dict | None:
    """Find the first order matching a customer email."""
    email_lower = email.lower().strip()
    for oid, order in ORDER_DATABASE.items():
        if order["customer_email"].lower() == email_lower:
            return {"order_id": oid, **order}
    return None
