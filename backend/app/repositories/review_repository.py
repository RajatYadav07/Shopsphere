from typing import Any, Dict, List, Optional, Tuple
from bson import ObjectId
from pymongo import DESCENDING
from pymongo.database import Database

from app.core.database import serialize_doc, serialize_docs, utc_now

class ReviewRepository:
    def __init__(self, db: Database):
        self.db = db
        self.collection = db["reviews"]
        self.products_collection = db["products"]
        self.customers_collection = db["customers"]

    def find_all(
        self,
        skip: int = 0,
        limit: int = 20,
        product_id: Optional[str] = None,
        rating: Optional[int] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        filter_query: Dict[str, Any] = {}
        if product_id:
            try:
                filter_query["product_id"] = ObjectId(product_id)
            except Exception:
                filter_query["product_id"] = product_id

        if rating:
            filter_query["rating"] = int(rating)

        total = self.collection.count_documents(filter_query)
        cursor = self.collection.find(filter_query).sort("created_at", DESCENDING).skip(skip).limit(limit)
        reviews = [serialize_doc(r) for r in cursor]

        # Hydrate product and customer names
        prod_ids = [ObjectId(r["product_id"]) for r in reviews if "product_id" in r and ObjectId.is_valid(str(r["product_id"]))]
        cust_ids = [ObjectId(r["customer_id"]) for r in reviews if "customer_id" in r and ObjectId.is_valid(str(r["customer_id"]))]

        prod_map = {str(p["_id"]): p.get("name") for p in self.products_collection.find({"_id": {"$in": prod_ids}})} if prod_ids else {}
        cust_map = {str(c["_id"]): c.get("name") for c in self.customers_collection.find({"_id": {"$in": cust_ids}})} if cust_ids else {}

        for r in reviews:
            r["product_name"] = prod_map.get(str(r.get("product_id")), "Unknown Product")
            r["customer_name"] = cust_map.get(str(r.get("customer_id")), "Verified Buyer")

        return reviews, total

    def find_by_id(self, review_id: str) -> Optional[Dict[str, Any]]:
        try:
            oid = ObjectId(review_id)
        except Exception:
            return None
        doc = self.collection.find_one({"_id": oid})
        return serialize_doc(doc)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data["product_id"] = ObjectId(data["product_id"])
        data["customer_id"] = ObjectId(data["customer_id"])
        data["created_at"] = utc_now()
        result = self.collection.insert_one(data)
        doc = self.collection.find_one({"_id": result.inserted_id})
        self.recalculate_product_ratings(str(data["product_id"]))
        return serialize_doc(doc)

    def update(self, review_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            oid = ObjectId(review_id)
        except Exception:
            return None
        clean_update = {k: v for k, v in update_data.items() if v is not None}
        if not clean_update:
            return self.find_by_id(review_id)
        clean_update["updated_at"] = utc_now()
        self.collection.update_one({"_id": oid}, {"$set": clean_update})
        updated = self.find_by_id(review_id)
        if updated and "product_id" in updated:
            self.recalculate_product_ratings(updated["product_id"])
        return updated

    def delete(self, review_id: str) -> bool:
        try:
            oid = ObjectId(review_id)
        except Exception:
            return False
        doc = self.collection.find_one({"_id": oid})
        if not doc:
            return False
        prod_id = str(doc.get("product_id"))
        res = self.collection.delete_one({"_id": oid})
        if res.deleted_count > 0:
            self.recalculate_product_ratings(prod_id)
            return True
        return False

    def recalculate_product_ratings(self, product_id: str) -> None:
        """Use aggregation to compute average rating and review count, then update the product."""
        try:
            p_oid = ObjectId(product_id)
        except Exception:
            return

        pipeline = [
            {"$match": {"product_id": p_oid}},
            {"$group": {
                "_id": "$product_id",
                "avg_rating": {"$avg": "$rating"},
                "review_count": {"$sum": 1}
            }}
        ]
        res = list(self.collection.aggregate(pipeline))
        if res:
            avg = round(float(res[0]["avg_rating"]), 2)
            cnt = int(res[0]["review_count"])
        else:
            avg = 0.0
            cnt = 0

        self.products_collection.update_one(
            {"_id": p_oid},
            {"$set": {"rating_average": avg, "review_count": cnt, "updated_at": utc_now()}}
        )
