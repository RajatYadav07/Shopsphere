from datetime import datetime
from typing import Any, Dict, List, Optional
from pymongo.database import Database

class AnalyticsRepository:
    def __init__(self, db: Database):
        self.db = db
        self.orders = db["orders"]
        self.products = db["products"]
        self.customers = db["customers"]
        self.reviews = db["reviews"]

    def get_dashboard_metrics(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        match_filter: Dict[str, Any] = {"status": {"$ne": "cancelled"}}

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
                match_filter["created_at"] = date_filter

        # Revenue and total valid orders aggregation
        rev_pipeline = [
            {"$match": match_filter},
            {"$group": {
                "_id": None,
                "total_revenue": {"$sum": "$subtotal"},
                "total_orders": {"$sum": 1},
                "avg_order_value": {"$avg": "$subtotal"}
            }}
        ]
        rev_res = list(self.orders.aggregate(rev_pipeline))
        total_rev = round(rev_res[0]["total_revenue"], 2) if rev_res else 0.0
        total_orders = rev_res[0]["total_orders"] if rev_res else 0
        avg_order_value = round(rev_res[0]["avg_order_value"], 2) if rev_res else 0.0

        total_customers = self.customers.count_documents({})
        total_products = self.products.count_documents({})
        pending_orders = self.orders.count_documents({"status": "pending"})
        low_stock = self.products.count_documents({"stock_quantity": {"$gt": 0, "$lte": 10}, "inventory_tracked": True})

        return {
            "total_revenue": total_rev,
            "total_orders": total_orders,
            "total_customers": total_customers,
            "total_products": total_products,
            "pending_orders": pending_orders,
            "low_stock_products_count": low_stock,
            "average_order_value": avg_order_value,
        }

    def get_monthly_revenue_trends(self) -> List[Dict[str, Any]]:
        pipeline = [
            {"$match": {"status": {"$ne": "cancelled"}}},
            {"$group": {
                "_id": {"$dateToString": {"format": "%Y-%m", "date": "$created_at"}},
                "revenue": {"$sum": "$subtotal"},
                "orders_count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}},
            {"$project": {
                "_id": 0,
                "month": "$_id",
                "revenue": {"$round": ["$revenue", 2]},
                "orders_count": 1
            }}
        ]
        return list(self.orders.aggregate(pipeline))

    def get_category_sales(self) -> List[Dict[str, Any]]:
        pipeline = [
            {"$match": {"status": {"$ne": "cancelled"}}},
            {"$unwind": "$items"},
            {"$group": {
                "_id": {"$ifNull": ["$items.category", "General Merchandise"]},
                "total_revenue": {"$sum": "$items.line_total"},
                "units_sold": {"$sum": "$items.quantity"},
                "order_count": {"$sum": 1}
            }},
            {"$project": {
                "_id": 0,
                "category": "$_id",
                "total_revenue": {"$round": ["$total_revenue", 2]},
                "units_sold": 1,
                "order_count": 1
            }},
            {"$sort": {"total_revenue": -1}}
        ]
        return list(self.orders.aggregate(pipeline))

    def get_top_selling_products(self, limit: int = 5) -> List[Dict[str, Any]]:
        pipeline = [
            {"$match": {"status": {"$ne": "cancelled"}}},
            {"$unwind": "$items"},
            {"$group": {
                "_id": "$items.product_id",
                "name": {"$first": "$items.name"},
                "sku": {"$first": "$items.sku"},
                "units_sold": {"$sum": "$items.quantity"},
                "total_revenue": {"$sum": "$items.line_total"}
            }},
            {"$sort": {"units_sold": -1}},
            {"$limit": limit},
            {"$lookup": {
                "from": "products",
                "let": {"pid": {"$toObjectId": "$_id"}},
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$_id", "$$pid"]}}},
                    {"$project": {"category": 1}}
                ],
                "as": "prod"
            }},
            {"$unwind": {"path": "$prod", "preserveNullAndEmptyArrays": True}},
            {"$project": {
                "_id": 0,
                "product_id": "$_id",
                "name": 1,
                "sku": 1,
                "category": {"$ifNull": ["$prod.category", "Electronics"]},
                "units_sold": 1,
                "total_revenue": {"$round": ["$total_revenue", 2]}
            }}
        ]
        return list(self.orders.aggregate(pipeline))

    def get_order_status_distribution(self) -> List[Dict[str, Any]]:
        total_orders = self.orders.count_documents({})
        if total_orders == 0:
            return []
        pipeline = [
            {"$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }},
            {"$project": {
                "_id": 0,
                "status": "$_id",
                "count": 1,
                "percentage": {"$round": [{"$multiply": [{"$divide": ["$count", total_orders]}, 100]}, 1]}
            }},
            {"$sort": {"count": -1}}
        ]
        return list(self.orders.aggregate(pipeline))

    def get_rating_distribution(self) -> List[Dict[str, Any]]:
        pipeline = [
            {"$group": {
                "_id": "$rating",
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}},
            {"$project": {
                "_id": 0,
                "rating": "$_id",
                "count": 1
            }}
        ]
        # Ensure ratings 1 through 5 are present
        res = {r["rating"]: r["count"] for r in self.reviews.aggregate(pipeline)}
        return [{"rating": score, "count": res.get(score, 0)} for score in range(1, 6)]

    def get_repeat_customer_metrics(self) -> Dict[str, Any]:
        pipeline = [
            {"$match": {"status": {"$ne": "cancelled"}}},
            {"$group": {
                "_id": "$customer_id",
                "order_count": {"$sum": 1}
            }}
        ]
        res = list(self.orders.aggregate(pipeline))
        total_with_orders = len(res)
        repeat_customers = sum(1 for c in res if c["order_count"] > 1)
        single_order_customers = total_with_orders - repeat_customers
        repeat_rate = round((repeat_customers / total_with_orders * 100), 1) if total_with_orders > 0 else 0.0
        avg_orders = round(sum(c["order_count"] for c in res) / total_with_orders, 2) if total_with_orders > 0 else 0.0

        return {
            "total_customers": total_with_orders,
            "repeat_customers": repeat_customers,
            "repeat_customer_rate": repeat_rate,
            "single_order_customers": single_order_customers,
            "average_orders_per_customer": avg_orders
        }
