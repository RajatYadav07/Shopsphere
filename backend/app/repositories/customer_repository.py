import re
from typing import Any, Dict, List, Optional, Tuple
from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from pymongo.database import Database

from app.core.database import serialize_doc, serialize_docs, utc_now

class CustomerRepository:
    def __init__(self, db: Database):
        self.db = db
        self.collection = db["customers"]
        self.orders_collection = db["orders"]

    def find_all(
        self,
        skip: int = 0,
        limit: int = 15,
        search: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        filter_query: Dict[str, Any] = {}
        if search:
            escaped = re.escape(search)
            filter_query["$or"] = [
                {"name": {"$regex": escaped, "$options": "i"}},
                {"email": {"$regex": escaped, "$options": "i"}},
                {"city": {"$regex": escaped, "$options": "i"}},
                {"phone": {"$regex": escaped, "$options": "i"}},
                {"external_id": {"$regex": escaped, "$options": "i"}},
                {"external_unique_id": {"$regex": escaped, "$options": "i"}},
            ]

        total = self.collection.count_documents(filter_query)
        cursor = self.collection.find(filter_query).sort("created_at", DESCENDING).skip(skip).limit(limit)
        customers = [serialize_doc(c) for c in cursor]

        # Enrich customers with real aggregate metrics
        customer_ids = [ObjectId(c["id"]) for c in customers if "id" in c]
        if customer_ids:
            pipeline = [
                {"$match": {"customer_id": {"$in": customer_ids}, "status": {"$ne": "cancelled"}}},
                {"$group": {
                    "_id": "$customer_id",
                    "total_spent": {"$sum": "$subtotal"},
                    "total_orders": {"$sum": 1}
                }}
            ]
            stats = {str(item["_id"]): item for item in self.orders_collection.aggregate(pipeline)}
            for c in customers:
                cid = c.get("id")
                c_stat = stats.get(cid, {})
                c["total_spent"] = round(c_stat.get("total_spent", 0.0), 2)
                c["total_orders"] = c_stat.get("total_orders", 0)
                c["average_order_value"] = round(c["total_spent"] / c["total_orders"], 2) if c["total_orders"] > 0 else 0.0

        return customers, total

    def find_by_id(self, customer_id: str) -> Optional[Dict[str, Any]]:
        try:
            oid = ObjectId(customer_id)
        except Exception:
            return None
        doc = self.collection.find_one({"_id": oid})
        if not doc:
            return None
        res = serialize_doc(doc)

        # Aggregate customer orders
        pipeline = [
            {"$match": {"customer_id": oid, "status": {"$ne": "cancelled"}}},
            {"$group": {
                "_id": "$customer_id",
                "total_spent": {"$sum": "$subtotal"},
                "total_orders": {"$sum": 1}
            }}
        ]
        stat_res = list(self.orders_collection.aggregate(pipeline))
        if stat_res:
            res["total_spent"] = round(stat_res[0]["total_spent"], 2)
            res["total_orders"] = stat_res[0]["total_orders"]
            res["average_order_value"] = round(res["total_spent"] / res["total_orders"], 2)
        else:
            res["total_spent"] = 0.0
            res["total_orders"] = 0
            res["average_order_value"] = 0.0

        # Fetch recent order history
        orders = list(self.orders_collection.find({"customer_id": oid}).sort("created_at", DESCENDING).limit(20))
        res["order_history"] = serialize_docs(orders)
        return res

    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        doc = self.collection.find_one({"email": email.strip().lower()})
        return serialize_doc(doc)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data["email"] = data["email"].strip().lower()
        data["created_at"] = utc_now()
        result = self.collection.insert_one(data)
        doc = self.collection.find_one({"_id": result.inserted_id})
        return serialize_doc(doc)

    def update(self, customer_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            oid = ObjectId(customer_id)
        except Exception:
            return None
        clean_update = {k: v for k, v in update_data.items() if v is not None}
        if "email" in clean_update:
            clean_update["email"] = clean_update["email"].strip().lower()
        if not clean_update:
            return self.find_by_id(customer_id)
        self.collection.update_one({"_id": oid}, {"$set": clean_update})
        return self.find_by_id(customer_id)

    def delete(self, customer_id: str) -> Tuple[bool, str]:
        try:
            oid = ObjectId(customer_id)
        except Exception:
            return False, "Invalid Customer ID"
        # Safeguard: prevent deleting customer with existing orders
        order_count = self.orders_collection.count_documents({"customer_id": oid})
        if order_count > 0:
            return False, f"Cannot delete customer with {order_count} existing orders. Archive customer or retain for audit history."
        res = self.collection.delete_one({"_id": oid})
        return res.deleted_count > 0, "Deleted successfully"
