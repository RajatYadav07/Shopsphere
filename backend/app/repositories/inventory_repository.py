from typing import Any, Dict, List, Optional, Tuple
from bson import ObjectId
from pymongo import DESCENDING
from pymongo.database import Database
from pymongo.client_session import ClientSession

from app.core.database import serialize_doc, serialize_docs, utc_now

class InventoryRepository:
    def __init__(self, db: Database):
        self.db = db
        self.collection = db["inventory_movements"]
        self.products_collection = db["products"]

    def record_movement(
        self,
        product_id: str,
        change_quantity: int,
        reason: str,
        related_order_id: Optional[str] = None,
        session: Optional[ClientSession] = None
    ) -> Dict[str, Any]:
        try:
            prod_oid = ObjectId(product_id)
        except Exception:
            prod_oid = product_id

        doc = {
            "product_id": prod_oid,
            "change_quantity": change_quantity,
            "reason": reason,
            "related_order_id": ObjectId(related_order_id) if related_order_id and ObjectId.is_valid(related_order_id) else related_order_id,
            "created_at": utc_now()
        }
        res = self.collection.insert_one(doc, session=session)
        created = self.collection.find_one({"_id": res.inserted_id}, session=session)
        return serialize_doc(created)

    def find_all(
        self,
        skip: int = 0,
        limit: int = 20,
        product_id: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        filter_query: Dict[str, Any] = {}
        if product_id:
            try:
                filter_query["product_id"] = ObjectId(product_id)
            except Exception:
                filter_query["product_id"] = product_id

        total = self.collection.count_documents(filter_query)
        cursor = self.collection.find(filter_query).sort("created_at", DESCENDING).skip(skip).limit(limit)
        movements = [serialize_doc(m) for m in cursor]

        # Hydrate with product name and SKU
        prod_ids = [ObjectId(m["product_id"]) for m in movements if "product_id" in m and ObjectId.is_valid(str(m["product_id"]))]
        if prod_ids:
            prod_map = {str(p["_id"]): p for p in self.products_collection.find({"_id": {"$in": prod_ids}})}
            for m in movements:
                pid = str(m.get("product_id"))
                if pid in prod_map:
                    m["product_name"] = prod_map[pid].get("name")
                    m["sku"] = prod_map[pid].get("sku")

        return movements, total
