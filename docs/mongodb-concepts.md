# ShopSphere: MongoDB Architecture & NoSQL Viva Guide
> **Course / Project:** College NoSQL & MongoDB Database Systems Project  
> **Specialization:** Data Science / Distributed Data Systems  
> **Application:** ShopSphere — Premium E-Commerce & Analytics Platform  
> **Database Version:** MongoDB Community Server 8.0+  
> **Driver:** PyMongo 4.x (Python 3.12, FastAPI)

---

## Table of Contents
1. [Executive Summary & Database Architecture](#1-executive-summary--database-architecture)
2. [Data Modeling: Embedded Documents vs. References](#2-data-modeling-embedded-documents-vs-references)
3. [CRUD Operations & Write Concerns](#3-crud-operations--write-concerns)
4. [Aggregation Pipeline Deep-Dive (8 Real Pipelines)](#4-aggregation-pipeline-deep-dive-8-real-pipelines)
5. [Indexing & Query Optimization with `explain("executionStats")`](#5-indexing--query-optimization-with-explainexecutionstats)
6. [Database-Level Schema Validation (`$jsonSchema`)](#6-database-level-schema-validation-jsonschema)
7. [Transactions & Concurrency Control (ACID vs Two-Phase Compensation)](#7-transactions--concurrency-control)
8. [Comprehensive Viva Voce Q&A Cheat Sheet (Top 25 Questions)](#8-comprehensive-viva-voce-qa-cheat-sheet)

---

## 1. Executive Summary & Database Architecture

ShopSphere is an enterprise-grade e-commerce and real-time analytics web application engineered on top of MongoDB Community Server. Unlike relational databases (RDBMS) which normalize data across dozens of foreign-key joined tables, ShopSphere leverages MongoDB's **flexible document model (BSON)**, embedded schemas for high-locality read performance, and reference-based modeling where data isolation and unbounded growth prevention are critical.

```
+---------------------------------------------------------------------------------------+
|                                    SHOPSPHERE SYSTEM                                  |
+---------------------------------------------------------------------------------------+
|  Frontend (React + Vite + TS)  <--->  Backend (FastAPI + PyMongo)                     |
|                                                  |                                    |
|                                       MongoDB 8.0 Community                           |
|                                 +-------------------------------+                     |
|                                 | Database: 'shopsphere'        |                     |
|                                 +-------------------------------+                     |
|                                 | - products                    |                     |
|                                 | - customers                   |                     |
|                                 | - orders (embedded items/addr)|                     |
|                                 | - reviews                     |                     |
|                                 | - inventory_movements         |                     |
|                                 | - shopsphere_demo (sandbox)   |                     |
|                                 +-------------------------------+                     |
+---------------------------------------------------------------------------------------+
```

### Key Technical Specifications
- **BSON (Binary JSON):** MongoDB stores records as BSON, supporting native types absent in standard JSON: `ObjectId`, `ISODate`, `Double`, `Int32`, `Int64`, `Decimal128`, and raw binary.
- **Document Size Limit:** Strict 16MB per document ceiling (BSON document maximum).
- **Storage Engine:** WiredTiger with Snappy block compression and memory checkpointing.
- **Index Architecture:** B-Tree indexing on primary `_id` and custom secondary/compound keys.

---

## 2. Data Modeling: Embedded Documents vs. References

One of the most important design questions in NoSQL data modeling is: **"Should this related entity be embedded as a nested sub-document/array, or referenced via an `ObjectId`?"**

ShopSphere demonstrates both paradigms based on real-world access patterns and volume characteristics:

| Entity Relationship | Modeling Strategy | Rationale & Trade-offs |
| :--- | :--- | :--- |
| **Order $\rightarrow$ Line Items** | **Embedded Array** | **Historical Snapshot Pattern:** An order item must preserve the exact price, SKU, and product name at the moment of checkout, even if the main product catalog changes later. Atomicity: The entire order with all items is inserted/read in a single I/O operation. Array bounded by real-world cart size ($< 100$ items), far below 16MB limit. |
| **Order $\rightarrow$ Shipping Address** | **Embedded Subdocument** | **Point-in-Time Address:** Addresses are tightly coupled to orders and do not change after shipment. Prevents complex joins when fulfilling orders. |
| **Order $\rightarrow$ Customer** | **Referenced (`customer_id`)** | **Normalization:** A customer can place hundreds or thousands of orders over their lifetime. Embedding all orders inside the customer document would lead to document growth, risk hitting the 16MB ceiling, and degrade customer update performance. |
| **Review $\rightarrow$ Product & Customer** | **Referenced (`product_id`, `customer_id`)** | **Unbounded Growth Pattern:** Popular products accumulate thousands of reviews. Storing reviews as an embedded array inside `products` causes frequent document re-allocation on disk. Storing reviews in a dedicated collection keeps product records compact and fast for catalog browsing. |
| **Inventory Movement $\rightarrow$ Product** | **Referenced (`product_id`)** | **Audit Trail:** Every stock increment, decrement, and order allocation produces an immutable ledger entry. Referencing allows infinite historical scalability. |

### Practical Code Illustration: Order Document
```json
{
  "_id": ObjectId("6ad0a6a5aae1a996ae0833e0"),
  "customer_id": ObjectId("6ad0a6a5aae1a996ae0833af"),
  "items": [
    {
      "product_id": ObjectId("6ad0a6a5aae1a996ae0832d3"),
      "product_name": "Apple Smart Ring Tracker",
      "sku": "AUDI-APP-0028",
      "unit_price": 307.69,
      "quantity": 2,
      "line_total": 615.38
    }
  ],
  "shipping_address": {
    "street": "742 Evergreen Terrace",
    "city": "Springfield",
    "state": "IL",
    "postal_code": "62704",
    "country": "USA"
  },
  "subtotal": 615.38,
  "status": "delivered",
  "created_at": ISODate("2026-10-14T07:52:45.234Z"),
  "updated_at": ISODate("2026-10-15T04:52:45.234Z")
}
```

---

## 3. CRUD Operations & Write Concerns

ShopSphere exposes complete, production-grade CRUD endpoints mapped directly to PyMongo collection methods:

### 1. Create Operations
- `insertOne(doc)`: Inserts a single document and automatically generates a unique 12-byte BSON `_id` if not supplied.
- `insertMany([doc1, doc2, ...], ordered=True)`: Batch inserts. In ShopSphere's seed pipeline, `insertMany` processes hundreds of products in a single round-trip, significantly reducing network latency.

```python
# Backend implementation in customer_repository.py
result = self.collection.insert_one(customer_data)
new_id = result.inserted_id  # Returns BSON ObjectId
```

### 2. Read Operations
- `find(filter, projection)`: Returns a cursor. ShopSphere applies `.skip(offset).limit(limit).sort(sort_field, direction)` for memory-efficient server-side pagination.
- `find_one(filter)`: Scans until the first matching document is found and terminates the cursor.

### 3. Update Operations
MongoDB provides atomic field update operators that modify documents without replacing them:
- `$set`: Sets a field value without modifying other attributes.
- `$inc`: Atomically increments or decrements numerical fields (e.g., product stock or review counts).
- `$currentDate`: Sets the updated timestamp to the current server date.

```python
# Atomically decrement product stock if sufficient inventory exists
result = db.products.update_one(
    {"_id": product_oid, "stock_quantity": {"$gte": requested_qty}},
    {
        "$inc": {"stock_quantity": -requested_qty},
        "$set": {"updated_at": datetime.now(timezone.utc)}
    }
)
```

### 4. Delete Operations
- `delete_one(filter)`: Removes the first matching document.
- `delete_many(filter)`: Bulk deletion matching query filters.
- **Referential Integrity Safeguards:** ShopSphere checks if dependent documents exist before deleting (e.g., verifying a customer has zero historical orders before permitting account deletion).

### Write Concerns
Write concern describes the level of acknowledgment requested from MongoDB for write operations:
- `w: 1`: Acknowledges when written to the standalone/primary memory (default).
- `j: true`: Acknowledges only after the write has been written to the on-disk journal (durability guarantee against sudden server power failure).
- `w: "majority"`: Used in replica sets to ensure writes are replicated to a majority of nodes before returning success.

---

## 4. Aggregation Pipeline Deep-Dive (8 Real Pipelines)

The MongoDB Aggregation Framework processes documents through multi-stage pipelines where the output of one stage becomes the input to the next.

ShopSphere implements **8 production-grade aggregation pipelines** accessible in real time via the **MongoDB Concepts Lab** and the **Analytics & Reports** module:

### Pipeline 1: Total Revenue by Category
**Purpose:** Calculates total sales revenue and units sold per product category by unwinding order items and grouping.
```javascript
[
  { "$match": { "status": { "$nin": ["cancelled"] } } },
  { "$unwind": "$items" },
  {
    "$group": {
      "_id": "$items.category",
      "total_revenue": { "$sum": "$items.line_total" },
      "units_sold": { "$sum": "$items.quantity" },
      "order_count": { "$sum": 1 }
    }
  },
  { "$sort": { "total_revenue": -1 } },
  {
    "$project": {
      "category": "$_id",
      "total_revenue": { "$round": ["$total_revenue", 2] },
      "units_sold": 1,
      "order_count": 1,
      "_id": 0
    }
  }
]
```

### Pipeline 2: Monthly Sales Trends
**Purpose:** Aggregates order volume and cumulative gross revenue grouped by Year-Month string (`YYYY-MM`).
```javascript
[
  { "$match": { "status": { "$nin": ["cancelled"] } } },
  {
    "$group": {
      "_id": { "$dateToString": { "format": "%Y-%m", "date": "$created_at" } },
      "revenue": { "$sum": "$subtotal" },
      "orders_count": { "$sum": 1 }
    }
  },
  { "$sort": { "_id": 1 } },
  {
    "$project": {
      "month": "$_id",
      "revenue": { "$round": ["$revenue", 2] },
      "orders_count": 1,
      "_id": 0
    }
  }
]
```

### Pipeline 3: Top-Selling Products
**Purpose:** Identifies top performers by volume and revenue across all confirmed line items.
```javascript
[
  { "$match": { "status": { "$nin": ["cancelled"] } } },
  { "$unwind": "$items" },
  {
    "$group": {
      "_id": "$items.product_id",
      "name": { "$first": "$items.product_name" },
      "sku": { "$first": "$items.sku" },
      "category": { "$first": "$items.category" },
      "units_sold": { "$sum": "$items.quantity" },
      "total_revenue": { "$sum": "$items.line_total" }
    }
  },
  { "$sort": { "units_sold": -1 } },
  { "$limit": 10 },
  {
    "$project": {
      "product_id": { "$toString": "$_id" },
      "name": 1,
      "sku": 1,
      "category": 1,
      "units_sold": 1,
      "total_revenue": { "$round": ["$total_revenue", 2] },
      "_id": 0
    }
  }
]
```

### Pipeline 4: Customer Spending Analysis
**Purpose:** Joins orders to customer records, computing lifetime value (LTV), total orders, and average spend per customer.
```javascript
[
  { "$match": { "status": { "$nin": ["cancelled"] } } },
  {
    "$group": {
      "_id": "$customer_id",
      "total_spent": { "$sum": "$subtotal" },
      "order_count": { "$sum": 1 }
    }
  },
  {
    "$lookup": {
      "from": "customers",
      "localField": "_id",
      "foreignField": "_id",
      "as": "customer_info"
    }
  },
  { "$unwind": { "path": "$customer_info", "preserveNullAndEmptyArrays": true } },
  { "$sort": { "total_spent": -1 } },
  { "$limit": 15 },
  {
    "$project": {
      "customer_id": { "$toString": "$_id" },
      "name": "$customer_info.name",
      "email": "$customer_info.email",
      "total_spent": { "$round": ["$total_spent", 2] },
      "order_count": 1,
      "avg_order_value": { "$round": [{ "$divide": ["$total_spent", "$order_count"] }, 2] },
      "_id": 0
    }
  }
]
```

### Pipeline 5: Order Status Distribution
**Purpose:** Aggregates order count and total dollar value segmented by workflow status (`pending`, `confirmed`, `shipped`, `delivered`, `cancelled`).
```javascript
[
  {
    "$group": {
      "_id": "$status",
      "count": { "$sum": 1 },
      "total_value": { "$sum": "$subtotal" }
    }
  },
  {
    "$project": {
      "status": "$_id",
      "count": 1,
      "total_value": { "$round": ["$total_value", 2] },
      "_id": 0
    }
  }
]
```

### Pipeline 6: Customer-Order Left Outer Join (`$lookup`)
**Purpose:** Emulates SQL `LEFT JOIN` by pulling recent orders for each customer into an array.
```javascript
[
  { "$limit": 10 },
  {
    "$lookup": {
      "from": "orders",
      "localField": "_id",
      "foreignField": "customer_id",
      "as": "customer_orders"
    }
  },
  {
    "$project": {
      "name": 1,
      "email": 1,
      "city": 1,
      "order_count": { "$size": "$customer_orders" },
      "recent_orders": { "$slice": ["$customer_orders", 3] }
    }
  }
]
```

### Pipeline 7: Product-Review Join and Derived Ratings
**Purpose:** Recomputes actual product average ratings and review distribution on the fly using `$lookup`.
```javascript
[
  { "$limit": 10 },
  {
    "$lookup": {
      "from": "reviews",
      "localField": "_id",
      "foreignField": "product_id",
      "as": "product_reviews"
    }
  },
  {
    "$project": {
      "name": 1,
      "sku": 1,
      "category": 1,
      "price": 1,
      "calculated_review_count": { "$size": "$product_reviews" },
      "calculated_avg_rating": {
        "$round": [{ "$ifNull": [{ "$avg": "$product_reviews.rating" }, 0] }, 1]
      }
    }
  }
]
```

### Pipeline 8: Multi-Faceted Analytics Summary (`$facet`)
**Purpose:** Executes multiple independent aggregation sub-pipelines across the entire dataset in a single database pass.
```javascript
[
  {
    "$facet": {
      "overall_stats": [
        {
          "$group": {
            "_id": null,
            "total_orders": { "$sum": 1 },
            "total_revenue": {
              "$sum": { "$cond": [{ "$ne": ["$status", "cancelled"] }, "$subtotal", 0] }
            },
            "avg_order_value": {
              "$avg": { "$cond": [{ "$ne": ["$status", "cancelled"] }, "$subtotal", null] }
            }
          }
        }
      ],
      "status_counts": [
        { "$group": { "_id": "$status", "count": { "$sum": 1 } } }
      ]
    }
  }
]
```

---

## 5. Indexing & Query Optimization with `explain("executionStats")`

Indexes in MongoDB use **B-Tree (Balanced Tree)** data structures to store a sorted representation of field values with pointers to disk storage locations. Without indexes, MongoDB must perform a **Collection Scan (COLLSCAN)**, loading every document from disk into memory to evaluate the query.

### ShopSphere Index Strategy

| Collection | Index Fields | Index Type | Business / Performance Rationale |
| :--- | :--- | :--- | :--- |
| `products` | `{ "sku": 1 }` | **Unique Single** | Guarantees uniqueness across all stock units. Fast O(log N) lookup during checkout. |
| `customers` | `{ "email": 1 }` | **Unique Single** | Prevents duplicate user registrations and supports instant user login lookups. |
| `products` | `{ "category": 1, "price": 1 }` | **Compound** | Supports catalog filtering (`category = 'Electronics'`) sorted by price. Follows the **ESR Rule (Equality, Sort, Range)**. |
| `orders` | `{ "status": 1, "created_at": -1 }` | **Compound** | Optimizes admin queries: "Show all pending orders sorted newest first". |
| `orders` | `{ "customer_id": 1 }` | **Single Secondary** | Accelerates customer order history lookups and `$lookup` pipeline joins. |
| `reviews` | `{ "product_id": 1 }` | **Single Secondary** | Accelerates fetching reviews for specific product detail pages. |
| `inventory` | `{ "product_id": 1, "created_at": -1 }` | **Compound** | Powers instant audit logs for specific products sorted chronologically. |

### The ESR (Equality, Sort, Range) Rule
When building compound indexes:
1. **Equality:** Put fields that are filtered by exact equality first (`category`).
2. **Sort:** Put fields that determine sort order second (`price`).
3. **Range:** Put fields with range filters (`$gt`, `$lt`, `$in`) last.

### Query Analysis via `explain("executionStats")`

ShopSphere provides an interactive query optimizer playground in the Concepts Lab. In MongoDB 8.0 / PyMongo 4.x, explain statistics are obtained using the database administrative command:
```python
db.command("explain", {"find": "products", "filter": {"sku": "AUDI-APP-0028"}}, verbosity="executionStats")
```

#### Comparison: Indexed Scan (IXSCAN) vs Collection Scan (COLLSCAN)

| Execution Metric | Indexed Query (`sku = '...'`) | Unindexed Query (`description = '...'`) | Interpretation |
| :--- | :--- | :--- | :--- |
| **Winning Plan Stage** | `FETCH` $\leftarrow$ `IXSCAN` | `COLLSCAN` | Indexed query traverses B-Tree index; unindexed query inspects every raw document. |
| **`nReturned`** | `1` | `1` | Both queries match exactly 1 target document. |
| **`totalKeysExamined`** | `1` | `0` | IXSCAN checked 1 B-tree key; COLLSCAN does not use an index. |
| **`totalDocsExamined`** | `1` | **112+ (All documents)** | **COLLSCAN examined 100% of collection!** In large datasets (e.g. 10M rows), this results in severe I/O thrashing. |
| **Efficiency Ratio (`nReturned / totalDocsExamined`)** | **1.0 (Optimal)** | **0.0089 (Poor)** | 1.0 indicates perfect index selectivity. |

---

## 6. Database-Level Schema Validation (`$jsonSchema`)

A common misconception is that "NoSQL means no schema." While MongoDB schemas are flexible, production systems enforce database-level validation to prevent malformed data from corrupting reports.

### ShopSphere Two-Tier Validation Architecture
1. **Application Tier (Pydantic v2):** Validates types, formats, and business rules inside FastAPI before database queries are formed.
2. **Database Tier (`$jsonSchema`):** Enforced by the MongoDB WiredTiger engine directly on disk. Even direct command-line insertions or external microservices are blocked if they violate schema constraints.

### Applied `$jsonSchema` Example: `products` Collection
```python
db.command({
    "collMod": "products",
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "sku", "category", "price", "stock_quantity"],
            "properties": {
                "name": { "bsonType": "string", "minLength": 2 },
                "sku": { "bsonType": "string", "minLength": 3 },
                "category": { "bsonType": "string" },
                "price": { "bsonType": ["double", "int", "decimal"], "minimum": 0.01 },
                "stock_quantity": { "bsonType": "int", "minimum": 0 },
                "rating_average": { "bsonType": ["double", "int"], "minimum": 0, "maximum": 5 }
            }
        }
    },
    "validationLevel": "strict",
    "validationAction": "error"
})
```

#### Rejection Behavior
When an operation attempts to insert a negative price or missing SKU, MongoDB returns:
```
WriteError: Document failed validation
Error Code: 121 (DocumentValidationFailure)
```

---

## 7. Transactions & Concurrency Control

### ACID Multi-Document Transactions in MongoDB
Starting in MongoDB 4.0 (Replica Sets) and 4.2 (Sharded Clusters), MongoDB supports multi-document distributed ACID transactions with snapshot isolation.
- **Atomicity:** All writes in the transaction succeed, or none do.
- **Consistency:** Violations of schema rules or unique indexes roll back the transaction.
- **Isolation:** Snapshot isolation ensures uncommitted writes are never seen by concurrent queries.
- **Durability:** Committed transactions persist to the WiredTiger write-ahead journal.

### Local Standalone Deployment Adaptation
By default, standard local MongoDB Community installations run in **standalone mode** (no replica set configured). MongoDB restricts `client.start_session().start_transaction()` to replica sets.

ShopSphere handles this dynamically:
1. **Dynamic Topology Detection:** `order_service.py` inspects `client.topology_description.topology_type`.
2. **If Replica Set Detected:** Executes a full MongoDB multi-document ACID transaction.
3. **If Standalone Detected:** Employs an **Atomic Two-Phase Reservation & Compensation Pattern**:
   - Evaluates stock availability atomically per product using conditional queries (`stock_quantity >= requested_qty`).
   - Atomically decrements inventory using `$inc: {"stock_quantity": -qty}`.
   - Logs an auditable entry in `inventory_movements`.
   - Inserts the order document.
   - **Compensating Rollback:** If order creation fails at any intermediate point, an automated compensation routine restores previously decremented stock and logs a compensating audit movement.

---

## 8. Comprehensive Viva Voce Q&A Cheat Sheet

### Q1: What is the difference between SQL (Relational) and NoSQL (Document) databases?
> **Answer:** SQL databases store data in rigid, tabular rows and columns with strict relational foreign keys, relying heavily on `JOIN` operations. NoSQL document databases like MongoDB store self-contained documents (BSON) with dynamic, polymorphic schemas. MongoDB optimizes for hierarchical data, read locality, and horizontal horizontal scaling (sharding).

### Q2: What is BSON, and how does it differ from standard JSON?
> **Answer:** BSON stands for Binary JSON. It is a binary-encoded serialization format used by MongoDB. Unlike JSON which only natively supports strings, numbers, booleans, and null, BSON provides rich data types including `ObjectId`, `Date`, `Int32`, `Int64`, `Decimal128`, and raw binary, while enabling faster traversal through length-prefixed fields.

### Q3: What is an `ObjectId` in MongoDB, and what is its internal composition?
> **Answer:** An `ObjectId` is a 12-byte unique BSON identifier consisting of:
> - **4 bytes:** Unix timestamp (seconds since epoch) representing document creation time.
> - **5 bytes:** Random value unique to the machine and process.
> - **3 bytes:** Incrementing counter, initialized to a random value.
> Because the first 4 bytes represent time, `ObjectId`s are roughly chronological and allow extracting creation timestamps without storing a separate date field.

### Q4: When should you embed documents vs. use references?
> **Answer:**
> - **Embed** when data has a 1-to-1 or bounded 1-to-Few relationship, is always queried together, and must be updated atomically (e.g., items in an order).
> - **Reference** when data has 1-to-Many or Many-to-Many relationships, the related list grows unboundedly (preventing the 16MB document limit), or entities need to be queried independently (e.g., products and user reviews).

### Q5: What is MongoDB's maximum document size limit, and why does it exist?
> **Answer:** The limit is 16 Megabytes. It prevents memory runaway, ensures documents fit comfortably within RAM caches, and stops network serialization bottlenecks. For files exceeding 16MB, MongoDB provides **GridFS**.

### Q6: What is a Collection Scan (COLLSCAN) vs. an Index Scan (IXSCAN)?
> **Answer:**
> - **COLLSCAN:** MongoDB scans every raw document sequentially in the collection from disk. Time complexity is $O(N)$.
> - **IXSCAN:** MongoDB traverses a balanced B-Tree index to find matching keys, then fetches only the required documents. Time complexity is $O(\log N)$.

### Q7: Explain the ESR rule in compound indexes.
> **Answer:** ESR stands for **Equality, Sort, Range**:
> 1. Fields filtered by exact value (`$eq`) come first.
> 2. Fields used for sorting (`$sort`) come second.
> 3. Fields with range filters (`$gt`, `$lt`, `$in`) come last.
> Following ESR enables MongoDB to satisfy both filtering and sorting directly from the index tree without an in-memory sort stage (`SORT_KEY_GENERATOR`).

### Q8: What does `explain("executionStats")` tell us?
> **Answer:** It provides actual execution telemetry:
> - `executionStages.stage`: Shows `IXSCAN`, `FETCH`, or `COLLSCAN`.
> - `nReturned`: Number of documents matching the query.
> - `totalKeysExamined`: Number of index keys traversed.
> - `totalDocsExamined`: Number of raw documents loaded from disk/cache.
> - **Ideal ratio:** `totalDocsExamined == nReturned`.

### Q9: What is the MongoDB Aggregation Framework?
> **Answer:** It is a data processing pipeline model where documents pass through sequential stages. Common stages include `$match` (filter), `$group` (summarize), `$project` (reshape), `$unwind` (deconstruct arrays), `$lookup` (left outer join), and `$facet` (multi-faceted processing).

### Q10: How does `$lookup` work in MongoDB?
> **Answer:** `$lookup` performs a left outer join between two collections within the same database. It matches a `localField` to a `foreignField` and attaches matching documents from the foreign collection as an array field in the current document.

### Q11: What is the purpose of `$unwind`?
> **Answer:** `$unwind` deconstructs an array field from input documents, outputting one document for each element in the array. This is required before grouping by array attributes (e.g., grouping order items by product category).

### Q12: What is `$facet` in aggregation?
> **Answer:** `$facet` processes multiple aggregation pipelines concurrently within a single stage on the same input documents. It is used to generate multi-dimensional dashboard reports (e.g., total sales and status breakdown) in a single round-trip.

### Q13: Does MongoDB support ACID transactions?
> **Answer:** Yes. Single-document operations are inherently atomic in MongoDB. Multi-document ACID transactions have been supported since MongoDB 4.0 in replica sets and 4.2 in sharded clusters, utilizing snapshot isolation.

### Q14: How does ShopSphere maintain transactional consistency on a local standalone MongoDB instance?
> **Answer:** Standalone instances do not support replica set transactions. ShopSphere implements an **Atomic Two-Phase Reservation with Compensating Rollback**: stock is decremented conditionally using atomic `$inc` with `$gte` queries; if order persistence fails, an automated compensating write restores the exact stock allocation.

### Q15: What is `$jsonSchema` validation in MongoDB?
> **Answer:** It is a database-level enforcement mechanism using JSON Schema draft 4 syntax. It validates data types, required fields, and numerical ranges at the database layer, rejecting non-conforming writes with a `DocumentValidationFailure` error (code 121).

### Q16: Why have schema validation at both the API level and database level?
> **Answer:** **Defense in Depth**: Application validation (Pydantic) provides clean, user-friendly HTTP 422 error messages; database validation (`$jsonSchema`) guarantees data integrity even if external scripts, bulk migrations, or buggy code bypass the API layer.

### Q17: What is an index prefix?
> **Answer:** Given a compound index on `{ category: 1, price: 1, rating: -1 }`, the prefixes are:
> - `{ category: 1 }`
> - `{ category: 1, price: 1 }`
> Queries filtering on `category` or `category + price` can use this index. A query filtering only on `price` cannot use this compound index efficiently.

### Q18: What is a covered query?
> **Answer:** A query is "covered" when all fields requested in the projection and query filter exist inside the index itself. MongoDB satisfies the query entirely from the B-Tree index without reading the document from disk (`totalDocsExamined: 0`).

### Q19: What is a write concern in MongoDB?
> **Answer:** It defines the level of durability acknowledgment requested from the server. For instance, `w: 1` acknowledges when the primary memory is updated, while `j: true` waits for the write-ahead journal to commit to disk.

### Q20: What is the WiredTiger storage engine?
> **Answer:** WiredTiger is MongoDB's default storage engine. It provides document-level concurrency control (optimistic concurrency), Snappy compression for data and indexes, and checkpointing to maintain crash-consistent state on disk.

### Q21: What is the difference between `$set` and full document replacement?
> **Answer:** `$set` modifies only specified fields, leaving other fields intact and saving network/disk bandwidth. Full replacement (`replace_one`) overwrites the entire document, which can accidentally erase attributes.

### Q22: What is the aggregation 100MB RAM limit, and how is it mitigated?
> **Answer:** By default, an individual pipeline stage cannot exceed 100MB of RAM. If exceeded, MongoDB aborts the query. It is mitigated by indexing the initial `$match` stage, placing `$project` early to shed unused fields, or passing `allowDiskUse=True` to permit temporary disk spills.

### Q23: How are dates handled and stored in MongoDB?
> **Answer:** MongoDB stores dates as 64-bit integers representing milliseconds since the Unix epoch (UTC). Drivers serialize them as BSON `ISODate`. In ShopSphere, all timestamps use explicit UTC (`datetime.now(timezone.utc)`).

### Q24: What is the Historical Snapshot Pattern used in ShopSphere orders?
> **Answer:** When an order is placed, line items copy the product's current name, SKU, and unit price into the order document. If the vendor later changes the product title or doubles the price, historical orders and invoices remain mathematically accurate and immutable.

### Q25: How does PyMongo handle ObjectId serialization to JSON?
> **Answer:** Python's standard `json` library does not recognize BSON `ObjectId` or `datetime`. ShopSphere implements a recursive serialization layer (`serialize_doc`) that converts `_id` and foreign `ObjectId` fields into standard hex strings and `datetime` into ISO 8601 strings.

### Q26: How did you design the ETL pipeline to import the relational Olist Brazilian E-Commerce dataset into MongoDB?
> **Answer:** In `backend/scripts/import_dataset.py`, we designed a robust streaming ETL pipeline that:
> 1. **Translates Portuguese metadata:** Uses `product_category_name_translation.csv` to map Portuguese categories into standardized English catalog categories.
> 2. **Denormalizes Relational Order Items into Embedded Documents:** Transforms multiple rows from `olist_order_items_dataset.csv` into an embedded array of item snapshots (`product_name`, `sku`, `unit_price`, `quantity`, `line_total`) inside each order document.
> 3. **Preserves Normalization where appropriate:** References customers via `customer_id` `ObjectId`s, preventing unbounded document growth.
> 4. **Enforces Data Types:** Converts string timestamps to BSON `ISODate` (UTC) and string prices to floating-point doubles matching `$jsonSchema` validators.
> 5. **Distinguishes Synthetic Data:** Since Olist is a third-party marketplace without warehouse inventory tracking, we explicitly generate synthetic inventory stock and movements tagged as `"source": "synthetic_olist_inventory"`, maintaining complete transparency.

---

*Authored for the ShopSphere Project — College MongoDB Viva & CV Portfolio Reference.*
