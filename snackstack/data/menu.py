
from __future__ import annotations

from typing import List
from snackstack.config import langchain_embedding
from langchain_chroma import Chroma
from langchain_core.documents import Document
from snackstack.logger import setup_logger

logger = setup_logger("vectore_store")

menu_data: List[dict] = [
    {
        "id": "FOOD001",
        "name": "Pasta",
        "category": "Italian",
        "price": 500,
        "rating": 4.4,
        "description": "Classic white sauce pasta with herbs and mushroom",
        "in_stock": True,
        "spice_level": 1
    },
    {
        "id": "FOOD002",
        "name": "Margherita Pizza",
        "category": "Italian",
        "price": 650,
        "rating": 4.6,
        "description": "Fresh mozzarella, basil, and tomato sauce pizza",
        "in_stock": True,
        "spice_level": 0
    },
    {
        "id": "FOOD003",
        "name": "Butter Chicken",
        "category": "Indian",
        "price": 550,
        "rating": 4.8,
        "description": "Creamy tomato-based chicken curry",
        "in_stock": True,
        "spice_level": 2
    },
    {
        "id": "FOOD004",
        "name": "Paneer Tikka",
        "category": "Indian",
        "price": 450,
        "rating": 4.5,
        "description": "Grilled cottage cheese cubes with spices",
        "in_stock": False,
        "spice_level": 2
    },
    {
        "id": "FOOD005",
        "name": "Veg Hakka Noodles",
        "category": "Chinese",
        "price": 400,
        "rating": 4.2,
        "description": "Stir-fried noodles with fresh vegetables",
        "in_stock": True,
        "spice_level": 1
    },
    {
        "id": "FOOD006",
        "name": "Chicken Manchurian",
        "category": "Chinese",
        "price": 520,
        "rating": 4.3,
        "description": "Chicken balls tossed in spicy Manchurian sauce",
        "in_stock": True,
        "spice_level": 3
    },
    {
        "id": "FOOD007",
        "name": "Veg Burger",
        "category": "American",
        "price": 250,
        "rating": 4.1,
        "description": "Crispy vegetable patty with fresh lettuce",
        "in_stock": True,
        "spice_level": 1
    },
    {
        "id": "FOOD008",
        "name": "Chocolate Brownie",
        "category": "Dessert",
        "price": 220,
        "rating": 4.7,
        "description": "Rich chocolate brownie served warm",
        "in_stock": True,
        "spice_level": 0
    }
]

PERSIST_DIR = "./rag_vectorstore"
COLLECTION_NAME = "menu_table"

def ingest_menu_data(data: List[dict]= menu_data) -> Chroma:

    try:
        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=langchain_embedding,
            persist_directory=PERSIST_DIR,
        )

        if vector_store._collection.count() > 0:
            logger.debug("Loaded vectore store")
            return vector_store

    except Exception:
        pass

    documents = []

    for doc in data:
        food_item = f"""
            name: {doc["name"]}
            category: {doc["category"]}
            price: {doc["price"]}
            rating: {doc["rating"]}
            description: {doc["description"]}
            spice_level: {doc["spice_level"]}
        """.strip()

        metadata = {
            "id": doc["id"],
            "name": doc["name"],
            "category": doc["category"],
            "price": doc["price"],
            "rating": doc["rating"],
            "description": doc["description"],
            "in_stock": doc["in_stock"],
            "spice_level": doc["spice_level"]
        }

        document = Document(page_content=food_item, metadata=metadata)
        documents.append(document)


    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=langchain_embedding,
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIR,
        collection_metadata={"hnsw:space": "cosine"}
    )

    
    logger.debug("Created vectore store")
    return vector_store


# if __name__ == "__main__":
#     vector_store = ingest_menu_data()

#     logger.info(
#         "Vector DB loaded. collection=%s count=%s",
#         COLLECTION_NAME,
#         vector_store._collection.count()
#     )

        