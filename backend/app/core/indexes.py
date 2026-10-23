import logging
from typing import Any, Dict, List
from pymongo import ASCENDING, DESCENDING, TEXT
from pymongo.database import Database

logger = logging.getLogger("shopsphere.indexes")

INDEX_DEFINITIONS = {
    "products": [
        {"keys": [("sku", ASCENDING)], "options": {"unique": True, "name": "uniq_sku"}},
        {"keys": [("external_id", ASCENDING)], "options": {"unique": True, "partialFilterExpression": {"external_id": {"$type": "string"}}, "name": "uniq_product_external_id"}},
        {"keys": [("category", ASCENDING), ("price", ASCENDING)], "options": {"name": "idx_category_price"}},
        {"keys": [("name", TEXT), ("brand", TEXT)], "options": {"name": "idx_name_brand_text"}},
        {"keys": [("created_at", DESCENDING)], "options": {"name": "idx_products_created_at"}},
    ],
    "customers": [
        {"keys": [("email", ASCENDING)], "options": {"unique": True, "partialFilterExpression": {"email": {"$type": "string"}}, "name": "uniq_customer_email"}},
        {"keys": [("external_id", ASCENDING)], "options": {"unique": True, "partialFilterExpression": {"external_id": {"$type": "string"}}, "name": "uniq_customer_external_id"}},
        {"keys": [("name", ASCENDING)], "options": {"name": "idx_customer_name"}},
        {"keys": [("created_at", DESCENDING)], "options": {"name": "idx_customers_created_at"}},
    ],
    "orders": [
        {"keys": [("external_id", ASCENDING)], "options": {"unique": True, "partialFilterExpression": {"external_id": {"$type": "string"}}, "name": "uniq_order_external_id"}},
        {"keys": [("status", ASCENDING), ("created_at", DESCENDING)], "options": {"name": "idx_orders_status_date"}},
        {"keys": [("customer_id", ASCENDING)], "options": {"name": "idx_orders_customer_id"}},
        {"keys": [("created_at", DESCENDING)], "options": {"name": "idx_orders_created_at"}},
        {"keys": [("source", ASCENDING)], "options": {"name": "idx_orders_source"}},
    ],
    "reviews": [
        {"keys": [("external_id", ASCENDING), ("product_id", ASCENDING)], "options": {"unique": True, "partialFilterExpression": {"external_id": {"$type": "string"}}, "name": "uniq_review_ext_prod"}},
        {"keys": [("product_id", ASCENDING)], "options": {"name": "idx_reviews_product_id"}},
        {"keys": [("customer_id", ASCENDING)], "options": {"name": "idx_reviews_customer_id"}},
        {"keys": [("order_id", ASCENDING)], "options": {"name": "idx_reviews_order_id"}},
        {"keys": [("created_at", DESCENDING)], "options": {"name": "idx_reviews_created_at"}},
    ],
    "inventory_movements": [
        {"keys": [("product_id", ASCENDING)], "options": {"name": "idx_inv_product_id"}},
        {"keys": [("created_at", DESCENDING)], "options": {"name": "idx_inv_created_at"}},
    ],
    "sellers": [
        {"keys": [("external_id", ASCENDING)], "options": {"unique": True, "partialFilterExpression": {"external_id": {"$type": "string"}}, "name": "uniq_seller_external_id"}},
        {"keys": [("city", ASCENDING)], "options": {"name": "idx_seller_city"}},
    ]
}

def create_all_indexes(db: Database) -> Dict[str, List[str]]:
    """Create all required indexes across collections idempotently."""
    results = {}
    for collection_name, indexes in INDEX_DEFINITIONS.items():
        results[collection_name] = []
        col = db[collection_name]
        for idx in indexes:
            try:
                idx_name = col.create_index(idx["keys"], **idx.get("options", {}))
                results[collection_name].append(idx_name)
                logger.info(f"Created/verified index '{idx_name}' on collection '{collection_name}'")
            except Exception as e:
                logger.warning(f"Error creating index on '{collection_name}': {e}")
                results[collection_name].append(f"FAILED: {e}")
    return results

def get_indexes_summary(db: Database) -> Dict[str, Any]:
    """Retrieve detailed index information across all collections for the Concepts Lab."""
    summary = {}
    collections = ["products", "customers", "orders", "reviews", "inventory_movements"]
    for col_name in collections:
        col = db[col_name]
        try:
            indexes = list(col.list_indexes())
            summary[col_name] = [
                {
                    "name": idx.get("name"),
                    "key": list(idx.get("key", {}).items()),
                    "unique": idx.get("unique", False),
                    "sparse": idx.get("sparse", False),
                }
                for idx in indexes
            ]
        except Exception as e:
            summary[col_name] = [{"error": str(e)}]
    return summary
