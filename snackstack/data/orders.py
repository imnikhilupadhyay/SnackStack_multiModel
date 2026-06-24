
from __future__ import annotations

from typing import Optional

order_data: dict[str, dict] = {
    "ORD101": {
        "food_item": "Margherita Pizza",
        "food_id": "FOOD002",
        "customer_email": "ram.sharma@example.com",
        "status": "Out for Delivery",
        "price": "650",
        "payment": "cod",
        "order_time": "18:30:54"
    },
    "ORD102": {
        "food_item": "Butter Chicken",
        "food_id": "FOOD003",
        "customer_email": "priya.verma@example.com",
        "status": "Preparing",
        "price": "550",
        "payment": "online",
        "order_time": "19:05:12"
    },
    "ORD103": {
        "food_item": "Veg Hakka Noodles",
        "food_id": "FOOD005",
        "customer_email": "amit.kumar@example.com",
        "status": "Delivered",
        "price": "400",
        "payment": "upi",
        "order_time": "17:45:30"
    },
    "ORD104": {
        "food_item": "Chocolate Brownie",
        "food_id": "FOOD008",
        "customer_email": "neha.gupta@example.com",
        "status": "Confirmed",
        "price": "220",
        "payment": "card",
        "order_time": "20:10:05"
    },
    "ORD105": {
        "food_item": "Veg Burger",
        "food_id": "FOOD007",
        "customer_email": "rohit.mehra@example.com",
        "status": "Cancelled",
        "price": "250",
        "payment": "refund_pending",
        "order_time": "16:55:47"
    },
    "ORD106": {
        "food_item": "Pasta",
        "food_id": "FOOD001",
        "customer_email": "sneha.jain@example.com",
        "status": "Delivered",
        "price": "500",
        "payment": "cod",
        "order_time": "15:22:18"
    }
}

def get_order_by_id(order_id: str) -> Optional[dict]:
    order_id = order_id.strip().upper()
    return order_data.get(order_id)
