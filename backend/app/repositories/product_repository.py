import re
from typing import Any, Dict, List, Optional, Tuple
from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from pymongo.database import Database
from pymongo.client_session import ClientSession

from app.core.database import serialize_doc, serialize_docs, utc_now

class ProductRepository:
    def __init__(self, db: Database):
        self.collection = db["products"]

    def find_all(
        self,
        skip: int = 0,
        limit: int = 12,
        search: Optional[str] = None,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        stock_status: Optional[str] = None, # 'in_stock', 'low_stock', 'out_of_stock'
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> Tuple[List[Dict[str, Any]], int]:
        filter_query: Dict[str, Any] = {}

        if search:
            escaped = re.escape(search)
            filter_query["$or"] = [
                {"name": {"$regex": escaped, "$options": "i"}},
                {"sku": {"$regex": escaped, "$options": "i"}},
                {"brand": {"$regex": escaped, "$options": "i"}},
                {"tags": {"$regex": escaped, "$options": "i"}}
            ]

        if category:
            filter_query["category"] = category

        if brand:
            filter_query["brand"] = brand

        if min_price is not None or max_price is not None:
            filter_query["price"] = {}
            if min_price is not None:
                filter_query["price"]["$gte"] = float(min_price)
            if max_price is not None:
                filter_query["price"]["$lte"] = float(max_price)

        if stock_status == "out_of_stock":
            filter_query["stock_quantity"] = 0
            filter_query["inventory_tracked"] = True
        elif stock_status == "low_stock":
            filter_query["stock_quantity"] = {"$gt": 0, "$lte": 10}
            filter_query["inventory_tracked"] = True
        elif stock_status == "in_stock":
            filter_query["$or"] = [
                {"stock_quantity": {"$gt": 0}},
                {"inventory_tracked": False}
            ]

        order = DESCENDING if sort_order.lower() == "desc" else ASCENDING
        sort_field = sort_by if sort_by in ["price", "name", "rating_average", "stock_quantity", "created_at"] else "created_at"

        total = self.collection.count_documents(filter_query)
        cursor = self.collection.find(filter_query).sort(sort_field, order).skip(skip).limit(limit)
        items = [serialize_doc(d) for d in cursor]
        return items, total

    def find_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        try:
            oid = ObjectId(product_id)
        except Exception:
            return None
        doc = self.collection.find_one({"_id": oid})
        return serialize_doc(doc)

    def find_by_sku(self, sku: str) -> Optional[Dict[str, Any]]:
        doc = self.collection.find_one({"sku": sku.strip().upper()})
        return serialize_doc(doc)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data["created_at"] = utc_now()
        data["updated_at"] = data["created_at"]
        data.setdefault("rating_average", 0.0)
        data.setdefault("review_count", 0)
        result = self.collection.insert_one(data)
        doc = self.collection.find_one({"_id": result.inserted_id})
        return serialize_doc(doc)

    def update(self, product_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            oid = ObjectId(product_id)
        except Exception:
            return None
        clean_update = {k: v for k, v in update_data.items() if v is not None}
        if not clean_update:
            return self.find_by_id(product_id)
        clean_update["updated_at"] = utc_now()
        self.collection.update_one({"_id": oid}, {"$set": clean_update})
        return self.find_by_id(product_id)

    def delete(self, product_id: str) -> bool:
        try:
            oid = ObjectId(product_id)
        except Exception:
            return False
        result = self.collection.delete_one({"_id": oid})
        return result.deleted_count > 0

    def adjust_stock(self, product_id: str, change: int, session: Optional[ClientSession] = None) -> bool:
        """Atomically change stock ensuring stock doesn't go below 0."""
        try:
            oid = ObjectId(product_id)
        except Exception:
            return False

        if change < 0:
            # Atomic decrement ensuring stock_quantity >= abs(change)
            query = {"_id": oid, "stock_quantity": {"$gte": abs(change)}}
        else:
            query = {"_id": oid}

        res = self.collection.update_one(
            query,
            {"$inc": {"stock_quantity": change}, "$set": {"updated_at": utc_now()}},
            session=session
        )
        return res.modified_count > 0

    def get_categories(self) -> List[str]:
        return sorted([c for c in self.collection.distinct("category") if c])

    def get_brands(self) -> List[str]:
        return sorted([b for b in self.collection.distinct("brand") if b])

    def count_low_stock(self, threshold: int = 10) -> int:
        return self.collection.count_documents({"stock_quantity": {"$gt": 0, "$lte": threshold}})
