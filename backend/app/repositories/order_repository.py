import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from bson import ObjectId
from pymongo import DESCENDING
from pymongo.database import Database
from pymongo.client_session import ClientSession

from app.core.database import serialize_doc, serialize_docs, utc_now

class OrderRepository:
    def __init__(self, db: Database):
        self.db = db
        self.collection = db["orders"]
        self.customers_collection = db["customers"]

    def find_all(
        self,
        skip: int = 0,
        limit: int = 15,
        search: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        filter_query: Dict[str, Any] = {}

        if status:
            filter_query["status"] = status.lower()

        if start_date or end_date:
            date_filter = {}
            if start_date:
                try:
                    date_filter["$gte"] = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
                except Exception:
                    pass
            if end_date:
                try:
                    date_filter["$lte"] = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                except Exception:
                    pass
            if date_filter:
                filter_query["created_at"] = date_filter

        if search:
            escaped = re.escape(search)
            # Find matching customer ObjectIds first
            matching_custs = self.customers_collection.find(
                {"$or": [{"name": {"$regex": escaped, "$options": "i"}}, {"email": {"$regex": escaped, "$options": "i"}}]},
                {"_id": 1}
            )
            matching_cust_ids = [c["_id"] for c in matching_custs]

            or_clauses: List[Dict[str, Any]] = [
                {"items.name": {"$regex": escaped, "$options": "i"}},
                {"items.sku": {"$regex": escaped, "$options": "i"}},
                {"external_id": {"$regex": escaped, "$options": "i"}},
            ]
            if ObjectId.is_valid(search):
                or_clauses.append({"_id": ObjectId(search)})
            if matching_cust_ids:
                or_clauses.append({"customer_id": {"$in": matching_cust_ids}})

            filter_query["$or"] = or_clauses

        total = self.collection.count_documents(filter_query)
        cursor = self.collection.find(filter_query).sort("created_at", DESCENDING).skip(skip).limit(limit)
        orders = [serialize_doc(o) for o in cursor]

        # Populate customer details
        cust_ids = [ObjectId(o["customer_id"]) for o in orders if "customer_id" in o and ObjectId.is_valid(o["customer_id"])]
        if cust_ids:
            cust_map = {str(c["_id"]): c for c in self.customers_collection.find({"_id": {"$in": cust_ids}})}
            for o in orders:
                cid = o.get("customer_id")
                if cid in cust_map:
                    o["customer_name"] = cust_map[cid].get("name")
                    o["customer_email"] = cust_map[cid].get("email")

        return orders, total

    def find_by_id(self, order_id: str) -> Optional[Dict[str, Any]]:
        try:
            oid = ObjectId(order_id)
        except Exception:
            return None
        doc = self.collection.find_one({"_id": oid})
        if not doc:
            return None
        order = serialize_doc(doc)
        if "customer_id" in order and ObjectId.is_valid(order["customer_id"]):
            cust = self.customers_collection.find_one({"_id": ObjectId(order["customer_id"])})
            if cust:
                order["customer"] = serialize_doc(cust)
                order["customer_name"] = cust.get("name")
                order["customer_email"] = cust.get("email")
        return order

    def create(self, order_data: Dict[str, Any], session: Optional[ClientSession] = None) -> Dict[str, Any]:
        result = self.collection.insert_one(order_data, session=session)
        doc = self.collection.find_one({"_id": result.inserted_id}, session=session)
        return serialize_doc(doc)

    def update_status(self, order_id: str, new_status: str, session: Optional[ClientSession] = None) -> bool:
        try:
            oid = ObjectId(order_id)
        except Exception:
            return False
        res = self.collection.update_one(
            {"_id": oid},
            {"$set": {"status": new_status, "updated_at": utc_now()}},
            session=session
        )
        return res.modified_count > 0

    def count_by_status(self, status: str) -> int:
        return self.collection.count_documents({"status": status.lower()})
