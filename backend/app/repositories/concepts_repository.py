import time
from typing import Any, Dict, List, Optional
from bson import ObjectId
from pymongo.database import Database
from pymongo.errors import OperationFailure, WriteError

from app.core.database import serialize_doc, serialize_docs, utc_now

class ConceptsRepository:
    def __init__(self, db: Database):
        self.db = db
        self.demo_col = db["shopsphere_demo"]
        self.orders_col = db["orders"]
        self.products_col = db["products"]
        self.customers_col = db["customers"]
        self.reviews_col = db["reviews"]

    # -------------------------------------------------------------
    # A. CRUD Operations on Isolated Collection
    # -------------------------------------------------------------
    def execute_crud_demo(self, operation: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = payload or {}
        start_time = time.perf_counter()

        if operation == "insertOne":
            doc = {
                "item_name": payload.get("item_name", "Wireless Mechanical Keyboard"),
                "category": payload.get("category", "Peripherals"),
                "price": float(payload.get("price", 89.99)),
                "stock": int(payload.get("stock", 25)),
                "created_at": utc_now()
            }
            res = self.demo_col.insert_one(doc)
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                "operation": "insertOne",
                "mongo_code": f'db.shopsphere_demo.insertOne({{\n  "item_name": "{doc["item_name"]}",\n  "category": "{doc["category"]}",\n  "price": {doc["price"]},\n  "stock": {doc["stock"]},\n  "created_at": ISODate()\n}})',
                "explanation": "insertOne inserts a single document into the collection and automatically assigns a unique _id ObjectId if not provided.",
                "execution_time_ms": round(elapsed, 2),
                "affected_count": 1,
                "result": {"inserted_id": str(res.inserted_id), "document": serialize_doc(doc)}
            }

        elif operation == "insertMany":
            docs = [
                {"item_name": "RGB Gaming Mouse", "category": "Peripherals", "price": 49.99, "stock": 40, "created_at": utc_now()},
                {"item_name": "USB-C Fast Charger 65W", "category": "Accessories", "price": 29.99, "stock": 65, "created_at": utc_now()},
                {"item_name": "Noise Cancelling Headphones", "category": "Audio", "price": 199.99, "stock": 15, "created_at": utc_now()}
            ]
            res = self.demo_col.insert_many(docs)
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                "operation": "insertMany",
                "mongo_code": 'db.shopsphere_demo.insertMany([\n  { "item_name": "RGB Gaming Mouse", "price": 49.99, "stock": 40 },\n  { "item_name": "USB-C Fast Charger 65W", "price": 29.99, "stock": 65 },\n  { "item_name": "Noise Cancelling Headphones", "price": 199.99, "stock": 15 }\n])',
                "explanation": "insertMany performs an atomic batch insert of multiple documents in a single round-trip network call.",
                "execution_time_ms": round(elapsed, 2),
                "affected_count": len(res.inserted_ids),
                "result": {"inserted_ids": [str(i) for i in res.inserted_ids], "count": len(res.inserted_ids)}
            }

        elif operation == "find":
            limit = int(payload.get("limit", 10))
            cursor = self.demo_col.find({}).sort("created_at", -1).limit(limit)
            docs = [serialize_doc(d) for d in cursor]
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                "operation": "find",
                "mongo_code": f'db.shopsphere_demo.find({{}}).sort({{ "created_at": -1 }}).limit({limit})',
                "explanation": "find() queries documents matching the filter criteria with optional sorting, projection, and pagination limit.",
                "execution_time_ms": round(elapsed, 2),
                "affected_count": len(docs),
                "result": docs
            }

        elif operation == "updateOne":
            filter_q = {"item_name": "Wireless Mechanical Keyboard"}
            # If not found, target any doc
            target = self.demo_col.find_one(filter_q) or self.demo_col.find_one({})
            if not target:
                # Seed one first so update succeeds
                self.demo_col.insert_one({"item_name": "Wireless Mechanical Keyboard", "category": "Peripherals", "price": 89.99, "stock": 25, "created_at": utc_now()})
                target = self.demo_col.find_one({})

            update_q = {"$inc": {"stock": 5}, "$set": {"updated_at": utc_now()}}
            res = self.demo_col.update_one({"_id": target["_id"]}, update_q)
            updated_doc = self.demo_col.find_one({"_id": target["_id"]})
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                "operation": "updateOne",
                "mongo_code": f'db.shopsphere_demo.updateOne(\n  {{ "_id": ObjectId("{str(target["_id"])}") }},\n  {{ "$inc": {{ "stock": 5 }}, "$set": {{ "updated_at": ISODate() }} }}\n)',
                "explanation": "updateOne applies atomic field updates (like $inc, $set) to the first document matching the query criteria.",
                "execution_time_ms": round(elapsed, 2),
                "affected_count": res.modified_count,
                "result": {"matched_count": res.matched_count, "modified_count": res.modified_count, "updated_document": serialize_doc(updated_doc)}
            }

        elif operation == "updateMany":
            filter_q = {"category": "Peripherals"}
            update_q = {"$inc": {"stock": 10}, "$set": {"last_restocked": utc_now()}}
            res = self.demo_col.update_many(filter_q, update_q)
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                "operation": "updateMany",
                "mongo_code": 'db.shopsphere_demo.updateMany(\n  { "category": "Peripherals" },\n  { "$inc": { "stock": 10 }, "$set": { "last_restocked": ISODate() } }\n)',
                "explanation": "updateMany updates all documents matching the filter criteria simultaneously across the collection.",
                "execution_time_ms": round(elapsed, 2),
                "affected_count": res.modified_count,
                "result": {"matched_count": res.matched_count, "modified_count": res.modified_count}
            }

        elif operation == "deleteOne":
            doc = self.demo_col.find_one({})
            if not doc:
                self.demo_col.insert_one({"item_name": "Temporary Demo Item", "price": 10.0, "stock": 1, "created_at": utc_now()})
                doc = self.demo_col.find_one({})
            target_id = doc["_id"]
            res = self.demo_col.delete_one({"_id": target_id})
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                "operation": "deleteOne",
                "mongo_code": f'db.shopsphere_demo.deleteOne({{ "_id": ObjectId("{str(target_id)}") }})',
                "explanation": "deleteOne deletes a single document matching the filter from the collection.",
                "execution_time_ms": round(elapsed, 2),
                "affected_count": res.deleted_count,
                "result": {"deleted_id": str(target_id), "deleted_count": res.deleted_count}
            }

        elif operation == "deleteMany":
            # Deletes all docs in isolated demo collection to demonstrate reset
            count_before = self.demo_col.count_documents({})
            res = self.demo_col.delete_many({})
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                "operation": "deleteMany",
                "mongo_code": 'db.shopsphere_demo.deleteMany({})',
                "explanation": "deleteMany deletes all matching documents from the collection. Here it safely resets the isolated demo sandbox.",
                "execution_time_ms": round(elapsed, 2),
                "affected_count": res.deleted_count,
                "result": {"documents_removed": res.deleted_count, "count_before": count_before}
            }

        else:
            raise ValueError(f"Unknown operation: {operation}")

    # -------------------------------------------------------------
    # B. Embedded Documents vs References Demonstration
    # -------------------------------------------------------------
    def get_modeling_comparison(self) -> Dict[str, Any]:
        sample_order = self.orders_col.find_one({})
        sample_customer = None
        if sample_order and "customer_id" in sample_order:
            sample_customer = self.customers_col.find_one({"_id": sample_order["customer_id"]})

        return {
            "embedded_model": {
                "concept": "Embedded Documents (Denormalization)",
                "example_collection": "orders",
                "embedded_fields": [
                    {
                        "field": "items",
                        "description": "Embedded array of purchased items containing snapshot of name, sku, unit_price, and quantity.",
                        "reason": "Guarantees historical integrity. Even if the product price changes in the catalog later, the customer's receipt remains immutable. Fetched in 1 single read without joins."
                    },
                    {
                        "field": "shipping_address",
                        "description": "Embedded sub-document containing street, city, state, postal_code.",
                        "reason": "1-to-1 strong coupling. A shipping address belongs strictly to this order instance."
                    }
                ],
                "sample_document": serialize_doc(sample_order),
                "pros": ["Zero network joins required (high read throughput)", "Atomic updates within a single document", "Historical data remains immutable"],
                "cons": ["16MB BSON document limit", "Data redundancy across documents"]
            },
            "referenced_model": {
                "concept": "Referenced Documents (Normalization)",
                "example_fields": [
                    {
                        "field": "orders.customer_id",
                        "references": "customers._id",
                        "description": "Each order stores only the ObjectId of the customer who placed it."
                    },
                    {
                        "field": "reviews.product_id",
                        "references": "products._id",
                        "description": "Each review stores an ObjectId reference to the product reviewed."
                    }
                ],
                "sample_referenced_customer": serialize_doc(sample_customer),
                "pros": ["Eliminates data duplication", "Easy customer updates (e.g., email change applies everywhere)", "Unlimited relationship scalability (avoids 16MB limit)"],
                "cons": ["Requires $lookup aggregation stages or multi-step queries to fetch combined views"]
            }
        }

    # -------------------------------------------------------------
    # C. Aggregation Pipeline Playground (8 Real Queries)
    # -------------------------------------------------------------
    def run_aggregation_playground(self, query_id: str) -> Dict[str, Any]:
        start = time.perf_counter()

        queries = {
            "1": {
                "title": "1. Total Revenue by Product Category",
                "stages": ["$match", "$unwind", "$lookup", "$group", "$sort", "$project"],
                "description": "Calculates revenue, units sold, and order count grouped by product category using an unwind and lookup join.",
                "pipeline": [
                    {"$match": {"status": {"$ne": "cancelled"}}},
                    {"$unwind": "$items"},
                    {"$lookup": {
                        "from": "products",
                        "let": {"pid": {"$toObjectId": "$items.product_id"}},
                        "pipeline": [
                            {"$match": {"$expr": {"$eq": ["$_id", "$$pid"]}}},
                            {"$project": {"category": 1}}
                        ],
                        "as": "product_info"
                    }},
                    {"$unwind": {"path": "$product_info", "preserveNullAndEmptyArrays": True}},
                    {"$group": {
                        "_id": {"$ifNull": ["$product_info.category", "General"]},
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
                ],
                "explanation": "Unwinds embedded items array, joins with products collection via $lookup to obtain category, then aggregates metrics using $group."
            },
            "2": {
                "title": "2. Monthly Sales Trends",
                "stages": ["$match", "$group", "$dateToString", "$sort", "$project"],
                "description": "Aggregates revenue and order counts by calendar month using MongoDB date expressions.",
                "pipeline": [
                    {"$match": {"status": {"$ne": "cancelled"}}},
                    {"$group": {
                        "_id": {"$dateToString": {"format": "%Y-%m", "date": "$created_at"}},
                        "total_revenue": {"$sum": "$subtotal"},
                        "order_count": {"$sum": 1}
                    }},
                    {"$sort": {"_id": 1}},
                    {"$project": {
                        "_id": 0,
                        "month": "$_id",
                        "total_revenue": {"$round": ["$total_revenue", 2]},
                        "order_count": 1
                    }}
                ],
                "explanation": "$dateToString extracts the year and month string from the ISODate timestamp, enabling time-series grouping."
            },
            "3": {
                "title": "3. Top-Selling Products by Volume",
                "stages": ["$match", "$unwind", "$group", "$sort", "$limit", "$project"],
                "description": "Finds the 5 highest-selling products based on quantity sold from embedded order items.",
                "pipeline": [
                    {"$match": {"status": {"$ne": "cancelled"}}},
                    {"$unwind": "$items"},
                    {"$group": {
                        "_id": "$items.product_id",
                        "product_name": {"$first": "$items.name"},
                        "sku": {"$first": "$items.sku"},
                        "units_sold": {"$sum": "$items.quantity"},
                        "total_revenue": {"$sum": "$items.line_total"}
                    }},
                    {"$sort": {"units_sold": -1}},
                    {"$limit": 5},
                    {"$project": {
                        "_id": 0,
                        "product_id": "$_id",
                        "product_name": 1,
                        "sku": 1,
                        "units_sold": 1,
                        "total_revenue": {"$round": ["$total_revenue", 2]}
                    }}
                ],
                "explanation": "$unwind decomposes array elements into individual documents; $group aggregates units sold per product, and $limit truncates to top 5."
            },
            "4": {
                "title": "4. Customer Spending Leaders",
                "stages": ["$match", "$group", "$lookup", "$unwind", "$sort", "$limit", "$project"],
                "description": "Joins customer references with orders to identify VIP customers by lifetime spend.",
                "pipeline": [
                    {"$match": {"status": {"$ne": "cancelled"}}},
                    {"$group": {
                        "_id": "$customer_id",
                        "total_spent": {"$sum": "$subtotal"},
                        "orders_placed": {"$sum": 1}
                    }},
                    {"$lookup": {
                        "from": "customers",
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "customer"
                    }},
                    {"$unwind": "$customer"},
                    {"$sort": {"total_spent": -1}},
                    {"$limit": 5},
                    {"$project": {
                        "_id": 0,
                        "customer_id": "$_id",
                        "customer_name": "$customer.name",
                        "email": "$customer.email",
                        "city": "$customer.city",
                        "total_spent": {"$round": ["$total_spent", 2]},
                        "orders_placed": 1
                    }}
                ],
                "explanation": "Demonstrates relational joining in MongoDB: $lookup matches customer_id from orders against _id in customers collection."
            },
            "5": {
                "title": "5. Order Status Distribution via $facet",
                "stages": ["$facet", "$group", "$project"],
                "description": "Uses multi-faceted aggregation ($facet) to simultaneously compute status breakdowns and total order volume.",
                "pipeline": [
                    {"$facet": {
                        "by_status": [
                            {"$group": {"_id": "$status", "count": {"$sum": 1}}},
                            {"$sort": {"count": -1}}
                        ],
                        "summary": [
                            {"$group": {
                                "_id": None,
                                "total_orders": {"$sum": 1},
                                "total_value": {"$sum": "$subtotal"},
                                "avg_value": {"$avg": "$subtotal"}
                            }},
                            {"$project": {
                                "_id": 0,
                                "total_orders": 1,
                                "total_value": {"$round": ["$total_value", 2]},
                                "avg_value": {"$round": ["$avg_value", 2]}
                            }}
                        ]
                    }}
                ],
                "explanation": "$facet processes multiple aggregation pipelines within a single stage on the same input documents, ideal for multi-widget dashboards."
            },
            "6": {
                "title": "6. Customer-Order Joins ($lookup & Embedded Match)",
                "stages": ["$lookup", "$match", "$project", "$limit"],
                "description": "Demonstrates embedding orders inside customer records via $lookup for customer profile screens.",
                "pipeline": [
                    {"$lookup": {
                        "from": "orders",
                        "localField": "_id",
                        "foreignField": "customer_id",
                        "as": "recent_orders"
                    }},
                    {"$match": {"recent_orders.0": {"$exists": True}}},
                    {"$project": {
                        "_id": 0,
                        "customer_id": "$_id",
                        "name": 1,
                        "email": 1,
                        "order_count": {"$size": "$recent_orders"},
                        "latest_order": {"$arrayElemAt": ["$recent_orders", 0]}
                    }},
                    {"$limit": 5}
                ],
                "explanation": "Populates an array field 'recent_orders' inside each customer record using $lookup without modifying storage."
            },
            "7": {
                "title": "7. Product-Review Joins and Computed Ratings",
                "stages": ["$lookup", "$unwind", "$group", "$sort", "$limit"],
                "description": "Joins products with reviews collection to compute dynamic ratings and reviews count on the fly.",
                "pipeline": [
                    {"$lookup": {
                        "from": "reviews",
                        "localField": "_id",
                        "foreignField": "product_id",
                        "as": "reviews"
                    }},
                    {"$match": {"reviews.0": {"$exists": True}}},
                    {"$project": {
                        "_id": 0,
                        "product_id": "$_id",
                        "name": 1,
                        "category": 1,
                        "price": 1,
                        "computed_review_count": {"$size": "$reviews"},
                        "computed_avg_rating": {"$round": [{"$avg": "$reviews.rating"}, 2]}
                    }},
                    {"$sort": {"computed_review_count": -1}},
                    {"$limit": 5}
                ],
                "explanation": "Verifies data consistency by calculating average ratings from raw review records dynamically via aggregation."
            },
            "8": {
                "title": "8. Average Order Value & Basket Sizing",
                "stages": ["$match", "$project", "$group"],
                "description": "Calculates average basket items and order value across all completed orders.",
                "pipeline": [
                    {"$match": {"status": {"$ne": "cancelled"}}},
                    {"$project": {
                        "subtotal": 1,
                        "item_count": {"$size": "$items"}
                    }},
                    {"$group": {
                        "_id": None,
                        "average_order_value": {"$avg": "$subtotal"},
                        "average_items_per_basket": {"$avg": "$item_count"},
                        "min_order_value": {"$min": "$subtotal"},
                        "max_order_value": {"$max": "$subtotal"}
                    }},
                    {"$project": {
                        "_id": 0,
                        "average_order_value": {"$round": ["$average_order_value", 2]},
                        "average_items_per_basket": {"$round": ["$average_items_per_basket", 2]},
                        "min_order_value": {"$round": ["$min_order_value", 2]},
                        "max_order_value": {"$round": ["$max_order_value", 2]}
                    }}
                ],
                "explanation": "$size computes array lengths per document, followed by mathematical accumulator functions ($avg, $min, $max)."
            }
        }

        q = queries.get(str(query_id))
        if not q:
            raise ValueError(f"Unknown query ID: {query_id}. Valid queries: 1 through 8.")

        # Determine target collection based on query
        target_col = self.orders_col
        if query_id in ["6"]:
            target_col = self.customers_col
        elif query_id in ["7"]:
            target_col = self.products_col

        cursor = target_col.aggregate(q["pipeline"])
        raw_result = list(cursor)
        elapsed = (time.perf_counter() - start) * 1000

        # Format pipeline code as clean string
        import json
        pipeline_code = f"db.{target_col.name}.aggregate([\n"
        pipeline_code += ",\n".join(["  " + json.dumps(stage) for stage in q["pipeline"]])
        pipeline_code += "\n])"

        return {
            "query_id": str(query_id),
            "title": q["title"],
            "description": q["description"],
            "stages_used": q["stages"],
            "pipeline_code": pipeline_code,
            "execution_time_ms": round(elapsed, 2),
            "result": serialize_docs(raw_result) if isinstance(raw_result, list) else raw_result,
            "explanation": q["explanation"]
        }

    # -------------------------------------------------------------
    # D. Indexing & Query Optimization (explain("executionStats"))
    # -------------------------------------------------------------
    def explain_query_execution(self, scenario: str, force_collscan: bool = False) -> Dict[str, Any]:
        """Run explain('executionStats') on real collection to show IXSCAN vs COLLSCAN."""
        if force_collscan:
            # Querying unindexed description or full collection scan
            col = self.products_col
            query = {"description": "Non-indexed full table scan demonstration text"}
            scenario_title = "Unindexed Field Query (Forced Full Collection Scan)"
        elif scenario == "find_by_sku":
            prod = self.products_col.find_one({}, {"sku": 1})
            sku = prod["sku"] if prod and "sku" in prod else "ELEC-SON-0001"
            col = self.products_col
            query = {"sku": sku}
            scenario_title = "Unique Index on SKU (B-Tree IXSCAN)"
        elif scenario == "category_price_filter":
            col = self.products_col
            query = {"category": "Electronics", "price": {"$gte": 50, "$lte": 300}}
            scenario_title = "Compound Index on Category & Price"
        elif scenario == "orders_status_date":
            col = self.orders_col
            query = {"status": "confirmed"}
            scenario_title = "Compound Index on Status & Date"
        else:
            col = self.products_col
            query = {"stock_quantity": {"$gt": 0}}
            scenario_title = "Stock Filter"

        explain_res = self.db.command(
            "explain",
            {"find": col.name, "filter": query},
            verbosity="executionStats"
        )
        exec_stats = explain_res.get("executionStats", {})
        query_planner = explain_res.get("queryPlanner", {})
        winning_plan = query_planner.get("winningPlan", {})

        def find_stage(plan: Dict[str, Any]) -> str:
            if not isinstance(plan, dict):
                return "UNKNOWN"
            stg = plan.get("stage", "")
            if "IXSCAN" in stg:
                return "IXSCAN"
            if "COLLSCAN" in stg:
                return "COLLSCAN"
            if "inputStage" in plan:
                return find_stage(plan["inputStage"])
            if "executionStages" in plan:
                return find_stage(plan["executionStages"])
            return stg or "UNKNOWN"

        stage = find_stage(exec_stats.get("executionStages", {})) or find_stage(winning_plan)
        is_ixscan = "IXSCAN" in stage

        index_name = None
        if is_ixscan:
            input_stage = winning_plan.get("inputStage", {})
            index_name = input_stage.get("indexName") or winning_plan.get("indexName") or exec_stats.get("executionStages", {}).get("indexName", "B-Tree Index")

        n_returned = exec_stats.get("nReturned", 0)
        total_keys = exec_stats.get("totalKeysExamined", 0)
        total_docs = exec_stats.get("totalDocsExamined", 0)
        exec_time = exec_stats.get("executionTimeMillis", 0.0)

        explanation = (
            f"Index Scan ({stage}) executed via index '{index_name or 'B-Tree'}'. Examined {total_keys} keys and {total_docs} docs."
            if is_ixscan else
            f"Collection Scan (COLLSCAN) occurred! Scanned all {total_docs} documents sequentially without an index."
        )

        return {
            "scenario": scenario_title,
            "query_filter": query,
            "index_used": index_name,
            "stage": stage,
            "nReturned": n_returned,
            "totalKeysExamined": total_keys,
            "totalDocsExamined": total_docs,
            "executionTimeMillis": float(exec_time),
            "is_index_scan": is_ixscan,
            "explanation": explanation,
            "raw_stats": {
                "nReturned": n_returned,
                "totalKeysExamined": total_keys,
                "totalDocsExamined": total_docs,
                "executionTimeMillis": exec_time,
                "stage": stage
            }
        }

    # -------------------------------------------------------------
    # E. Schema Validation Demonstration
    # -------------------------------------------------------------
    def test_schema_validation(self, test_type: str, price: float, stock: int, item_name: str) -> Dict[str, Any]:
        """Demonstrate MongoDB collection validator acceptance vs rejection."""
        doc = {
            "item_name": item_name,
            "price": price,
            "stock": stock
        }

        if test_type == "valid":
            try:
                res = self.demo_col.insert_one(doc)
                return {
                    "test_type": "valid",
                    "document_attempted": serialize_doc(doc),
                    "accepted": True,
                    "status_message": f"Successfully inserted document with _id: {str(res.inserted_id)}",
                    "mongodb_error": None,
                    "explanation": "Document passed all MongoDB $jsonSchema rules: item_name is string, price is positive number >= 1.0, and stock is non-negative int >= 0."
                }
            except Exception as e:
                return {
                    "test_type": "valid",
                    "document_attempted": serialize_doc(doc),
                    "accepted": False,
                    "status_message": "Unexpected error",
                    "mongodb_error": str(e),
                    "explanation": "Validation error occurred."
                }
        else:
            invalid_doc = dict(doc)
            if invalid_doc.get("price", 0) > 0:
                invalid_doc["price"] = -45.00 # Violates minimum: 1.0 rule!

            try:
                self.demo_col.insert_one(invalid_doc)
                return {
                    "test_type": "invalid",
                    "document_attempted": serialize_doc(invalid_doc),
                    "accepted": True,
                    "status_message": "Warning: Collection validator did not reject document.",
                    "mongodb_error": None,
                    "explanation": "Validator did not trigger."
                }
            except (WriteError, OperationFailure) as e:
                return {
                    "test_type": "invalid",
                    "document_attempted": serialize_doc(invalid_doc),
                    "accepted": False,
                    "status_message": "Database write REJECTED by MongoDB $jsonSchema Validator (Error code: 121 - DocumentValidationFailure)",
                    "mongodb_error": str(e),
                    "explanation": "MongoDB rejected this write directly at the database engine level because 'price: -45.00' violates the rule 'minimum: 1.0'. Unlike API-level Pydantic validation, MongoDB schema validation protects data integrity even if queries bypass the backend API (e.g. via direct mongosh access)."
                }
            except Exception as e:
                return {
                    "test_type": "invalid",
                    "document_attempted": serialize_doc(invalid_doc),
                    "accepted": False,
                    "status_message": "Database write rejected",
                    "mongodb_error": str(e),
                    "explanation": "Database rejected document."
                }
