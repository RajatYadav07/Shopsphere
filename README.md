# ShopSphere: Premium E-Commerce & MongoDB Analytics Platform

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React_18_+_TypeScript-61DAFB?style=flat&logo=react)](https://react.dev)
[![Vite](https://img.shields.io/badge/Bundler-Vite_8-646CFF?style=flat&logo=vite)](https://vitejs.dev)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css)](https://tailwindcss.com)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB_Community_8.0-47A248?style=flat&logo=mongodb)](https://www.mongodb.com)
[![PyMongo](https://img.shields.io/badge/Driver-PyMongo_4.x-green)](https://pymongo.readthedocs.io)
[![Tests](https://img.shields.io/badge/Tests-Pytest_Passing-brightgreen)](https://pytest.org)

ShopSphere is an enterprise-grade full-stack web application engineered to demonstrate advanced **NoSQL document modeling**, **real-time MongoDB aggregation pipelines**, **B-Tree index query optimization (`explain("executionStats")`)**, **database-level `$jsonSchema` validation**, and **two-phase transactional inventory management** on **MongoDB Community Server**.

Designed as a premier College NoSQL/MongoDB Database Systems project and a technical portfolio showcase.

---

## 🌟 Key Features

1. **Executive SaaS Analytics Dashboard:**
   - Real-time MongoDB aggregation metrics: Gross Revenue, Total Orders, Active Customers, Catalog Size, Low-Stock items.
   - Interactive Recharts: Monthly Sales Trends, Category Revenue Breakdown, Top 5 Performing Products, Recent Order Ledger.
2. **Full Product Catalog Management:**
   - Grid and Table views with server-side pagination, search by SKU/name, category & brand filtering, price ranges, and stock-status badges.
   - Prevent duplicate SKUs through a unique MongoDB index.
3. **Customer Relationship Management (CRM):**
   - Customer profiles, unique email constraints, city-based segmentation, and aggregated customer lifetime value (LTV).
4. **Transactional Order Management:**
   - Order placement with historical price/item snapshots.
   - Embedded shipping addresses and atomic stock decrement.
   - Order cancellation with automatic stock restoration and auditable inventory movement entries.
   - Multi-document ACID transactions with automatic fallback to two-phase compensation on standalone instances.
5. **Real-time Inventory & Audit Log:**
   - Live inventory status with low-stock warnings ($< 10$ units).
   - Stock-in / stock-out manual adjustments with permanent ledger entries in `inventory_movements`.
6. **Customer Reviews & Rating Aggregation:**
   - 1-to-5 star ratings with live product rating recalculation.
7. **Interactive MongoDB Concepts Lab (Viva Showcase):**
   - **CRUD Operations Sandbox:** Interactive execution of `insertOne`, `insertMany`, `find`, `updateOne`, `updateMany`, `deleteOne`, and `deleteMany` against an isolated sandbox collection (`shopsphere_demo`).
   - **Embedding vs Referencing Visualizer:** Demonstrates order item snapshots and customer references with architectural trade-off comparisons.
   - **Aggregation Playground:** 8 real aggregation pipelines executable with a single click, showing raw pipeline JSON, output, and natural-language explanations.
   - **Index & Explain Optimizer:** Compares `COLLSCAN` vs `IXSCAN` using live `explain("executionStats")`, showing `totalDocsExamined`, `totalKeysExamined`, and `nReturned`.
   - **Schema Validation Testing:** Demonstrates MongoDB `$jsonSchema` engine rejecting invalid writes at the database layer.
8. **Customer-Facing Storefront:**
   - Seamless toggle to a customer shopping experience with category filters, live cart management, and real MongoDB order checkout.

---

## 🏗️ System Architecture

```
                       +-----------------------------------+
                       |    React + Vite + TypeScript      |
                       |  (Tailwind CSS + Lucide + Recharts|
                       |       http://127.0.0.1:5173       |
                       +-----------------+-----------------+
                                         |  Axios HTTP / JSON
                                         v
                       +-----------------------------------+
                       |         FastAPI Backend           |
                       |       (Python 3.12 / Pydantic)    |
                       |       http://127.0.0.1:8000       |
                       +-----------------+-----------------+
                                         |  PyMongo 4.x
                                         v
                       +-----------------------------------+
                       |    MongoDB Community Server 8.0   |
                       |       mongodb://127.0.0.1:27017   |
                       |         Database: 'shopsphere'    |
                       +-----------------+-----------------+
                                         |
     +-------------------+---------------+-------------------+-------------------+
     |                   |               |                   |                   |
     v                   v               v                   v                   v
[products]          [customers]       [orders]           [reviews]     [inventory_movements]
- Unique SKU        - Unique Email    - Embedded Items   - Foreign Keys  - Immutable Ledger
- Compound Idx                        - Embedded Addr    - Rating Avg
```

---

## 💻 Tech Stack

- **Frontend:** React 18, Vite 8, TypeScript, Tailwind CSS, Lucide React, Recharts, Axios.
- **Backend:** Python 3.12, FastAPI, Pydantic v2, PyMongo 4.x, Uvicorn.
- **Database:** MongoDB Community Server 8.0+ running locally on Windows.
- **Testing:** Pytest, HTTPX.
- **Documentation:** Swagger UI (`/docs`), ReDoc (`/redoc`), and Markdown Viva Guide.

---

## 🚀 Quick Start Guide (Windows)

### Prerequisites
1. **MongoDB Community Server:** Running locally on port `27017`.
   - Verify in PowerShell:
     ```powershell
     mongosh --eval "db.version()"
     ```
2. **Python 3.10+** (Python 3.12 recommended).
3. **Node.js 18+** and `npm`.

---

### Step 1: Clone or Navigate to the Workspace
```powershell
cd d:\Mongo_db-project\ShopSphere
```

### Step 2: Set Up the Backend
1. Open PowerShell and navigate to the backend folder:
   ```powershell
   cd d:\Mongo_db-project\ShopSphere\backend
   ```
2. Create and activate a Python virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Verify environment settings (`backend/.env` is pre-configured):
   ```env
   MONGODB_URI=mongodb://127.0.0.1:27017/
   DATABASE_NAME=shopsphere
   BACKEND_HOST=127.0.0.1
   BACKEND_PORT=8000
   ```

### Step 3: Populate Database with Authentic Olist Brazilian E-Commerce Dataset

ShopSphere is configured to run against the **Olist Brazilian E-Commerce Public Dataset** in a dedicated database named **`shopsphere_olist`**, leaving the original demonstration database (`shopsphere`) completely untouched.

#### Dataset Attribution & Source:
- **Kaggle Source:** [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **Local Raw Files Directory:** `ShopSphere/data/olist/raw/`
  1. `olist_customers_dataset.csv` (99,441 rows)
  2. `olist_geolocation_dataset.csv` (1,000,163 rows)
  3. `olist_order_items_dataset.csv` (112,650 rows)
  4. `olist_order_payments_dataset.csv` (103,886 rows)
  5. `olist_order_reviews_dataset.csv` (99,224 rows)
  6. `olist_orders_dataset.csv` (99,441 rows)
  7. `olist_products_dataset.csv` (32,951 rows)
  8. `olist_sellers_dataset.csv` (3,095 rows)
  9. `product_category_name_translation.csv` (71 rows)

#### Run the Importer:
```powershell
cd d:\Mongo_db-project\ShopSphere\backend
.\venv\Scripts\Activate.ps1
python scripts\import_dataset.py --db-name shopsphere_olist
```

*CLI Options:*
- `--db-name <name>`: Target MongoDB database name (default: `shopsphere_olist`).
- `--data-dir <path>`: Path to directory containing raw CSV files (default: auto-detects `ShopSphere/data/olist/raw/`).
- `--limit-orders <N>`: Limit number of orders to import (default: `0` for all 99k+ orders).
- `--limit-products <N>`: Limit number of products to import (default: `0` for all 32k+ products).
- `--clear-existing-olist`: Removes previous Olist records in the target database before re-importing.

#### Verified MongoDB Collection Counts (`shopsphere_olist`):
| Collection Name | Document Count | Source / Description |
| :--- | :--- | :--- |
| **`products`** | **32,951** | Authentic catalog items with category translation and computed average ratings |
| **`customers`** | **99,441** | Brazilian customer records preserved with anonymized emails (`null`) and city/state |
| **`orders`** | **98,666** | Orders with embedded line items, payments, shipping CEP, and order timestamps (775 skipped due to 0 items) |
| **`reviews`** | **97,709** | Authentic review ratings (1-5 stars) and Portuguese review text |
| **`sellers`** | **3,095** | Brazilian marketplace seller directory with postal codes and state/city |
| **`inventory_movements`** | **0** | Clean ledger; reserved for operational store movements and demo orders |

---

## 🗃️ Olist Brazilian E-Commerce Preprocessing & Data Mapping Reference

The importer ([`backend/scripts/import_dataset.py`](backend/scripts/import_dataset.py)) parses and normalizes the relational Kaggle CSV files into ShopSphere's MongoDB document model:

| Olist CSV Source & Fields | ShopSphere MongoDB Collection & Target Fields | Transformation & Preprocessing Logic |
| :--- | :--- | :--- |
| `olist_products_dataset.csv`<br>+ `product_category_name_translation.csv` | **`products`**<br>- `_id` (`ObjectId`, deterministic)<br>- `external_id` (`String`)<br>- `name` (`String`)<br>- `sku` (`String`, Unique Index)<br>- `category` (`String`)<br>- `price` (`Double`)<br>- `stock_quantity` (`0`)<br>- `inventory_tracked` (`false`)<br>- `rating_average` (`Double`)<br>- `review_count` (`Int32`)<br>- `source` (`"olist_real"`) | Handles UTF-8 BOM encoding. Translates Portuguese category names to English. Generates clean deterministic SKUs (`OLIST-<CAT>-<HASH>`). Flags `inventory_tracked: false` without inventing fake stock quantities. |
| `olist_customers_dataset.csv`<br>- `customer_id`<br>- `customer_unique_id`<br>- `customer_city`<br>- `customer_state`<br>- `customer_zip_code_prefix` | **`customers`**<br>- `_id` (`ObjectId`, deterministic)<br>- `external_id` (`String`)<br>- `external_unique_id` (`String`)<br>- `name` (`String`)<br>- `email` (`null`)<br>- `city` (`String`)<br>- `state` (`String`)<br>- `source` (`"olist_real"`) | Preserves original customer and unique customer IDs. Does NOT fabricate fake email addresses or phone numbers. Uses partial unique index on email to allow multiple authentic anonymized records. |
| `olist_orders_dataset.csv`<br>+ `olist_order_items_dataset.csv`<br>+ `olist_order_payments_dataset.csv` | **`orders`**<br>- `_id` (`ObjectId`, deterministic)<br>- `external_id` (`String`)<br>- `customer_id` (`ObjectId`, Ref)<br>- `items` (`Array` of Embedded Docs)<br>- `payments` (`Array` of Subdocs)<br>- `shipping_address` (`Embedded Subdoc`)<br>- `freight_total` (`Double`)<br>- `subtotal` (`Double`)<br>- `total_amount` (`Double`)<br>- `status` (`String`)<br>- `is_historical` (`true`)<br>- `source` (`"olist_real"`) | In-memory pre-aggregation embeds items and payment installments directly into the order document. 775 orders with 0 items are omitted to satisfy `$jsonSchema` (`minItems: 1`). Marked `is_historical: true` (immutable). |
| `olist_order_reviews_dataset.csv`<br>- `review_id`<br>- `order_id`<br>- `review_score`<br>- `review_comment_message`<br>- `review_creation_date` | **`reviews`**<br>- `_id` (`ObjectId`, deterministic)<br>- `external_id` (`String`)<br>- `product_id` (`ObjectId`, Ref)<br>- `customer_id` (`ObjectId`, Ref)<br>- `order_id` (`ObjectId`, Ref)<br>- `rating` (`Int32`, 1-5)<br>- `review_text` (`String`) | Review IDs are keyed by `(external_id, product_id)` to resolve duplicate review IDs across orders. Recalculates product rating averages and review counts in bulk. |
| `olist_sellers_dataset.csv` | **`sellers`**<br>- `_id` (`ObjectId`, deterministic)<br>- `external_id` (`String`)<br>- `seller_zip_code_prefix`<br>- `city`<br>- `state` | Stored in dedicated `sellers` collection with unique index on `external_id`. |

---

## 🔒 Architectural Principles & Known Limitations

1. **No Invented Inventory or Contact Data:**
   - The public Olist dataset does not record warehouse inventory levels or customer personal contact details.
   - Products are marked `inventory_tracked: false` with `stock_quantity: 0`.
   - Customer emails are stored as `null` with a MongoDB partial unique index (`partialFilterExpression: {"email": {"$type": "string"}}`).
2. **Historical Transaction Immutability:**
   - Historical Olist orders are marked `is_historical: true` and `source: "olist_real"`.
   - Any attempt to modify order status or cancel a historical order via the API is rejected with HTTP 400: *"Cannot modify historical Olist transaction. Historical dataset records are immutable."*
3. **Demo & Test Isolation:**
   - New checkout transactions created via the Storefront or API are tagged `source: "demo"` and `is_historical: false`.
   - All automated unit and integration tests run against an isolated database named `shopsphere_test`, ensuring zero test artifacts are written to `shopsphere_olist` or `shopsphere`.

### Step 4: Run Automated Tests
Verify all database constraints, unique indexes, transactions, aggregation pipelines, and Olist import pipelines:
```powershell
pytest -v
```
*(All 12 tests should pass against isolated `shopsphere_test`).*

### Step 5: Start the Backend Server
```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- Interactive API Docs (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- API Health Check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

### Step 6: Set Up and Start the Frontend
1. Open a **new** PowerShell terminal:
   ```powershell
   cd d:\Mongo_db-project\ShopSphere\frontend
   ```
2. Install frontend packages:
   ```powershell
   npm install
   ```
3. Start the Vite development server:
   ```powershell
   npm run dev -- --host 127.0.0.1 --port 5173
   ```
4. Open your browser and navigate to:
   👉 **[http://127.0.0.1:5173](http://127.0.0.1:5173)**

---

## 🗃️ Olist Brazilian E-Commerce Data Mapping Reference

The importer ([`backend/scripts/import_dataset.py`](backend/scripts/import_dataset.py)) parses and normalizes the relational Kaggle CSV files into ShopSphere's MongoDB document model:

| Olist CSV Source & Fields | ShopSphere MongoDB Collection & Target Fields | Transformation / Business Logic |
| :--- | :--- | :--- |
| `olist_products_dataset.csv`<br>+ `product_category_name_translation.csv` | **`products`**<br>- `_id` (`ObjectId`)<br>- `name` (`String`)<br>- `sku` (`String`, Unique Index)<br>- `category` (`String`)<br>- `price` (`Double`)<br>- `stock_quantity` (`Int32`)<br>- `rating_average` (`Double`)<br>- `review_count` (`Int32`)<br>- `source` (`"olist_real"`) | Portuguese categories translated to English (e.g. `relogios_presentes` $\rightarrow$ `Watches & Gifts`). Deterministic SKU generated (`OLIST-WAGI-P1001`). Price calculated from actual median order items. Initial synthetic stock assigned and flagged. |
| `olist_customers_dataset.csv`<br>- `customer_id`<br>- `customer_unique_id`<br>- `customer_city`<br>- `customer_state`<br>- `customer_zip_code_prefix` | **`customers`**<br>- `_id` (`ObjectId`)<br>- `name` (`String`)<br>- `email` (`String`, Unique Index)<br>- `city` (`String`)<br>- `state` (`String`)<br>- `address` (`String`)<br>- `source` (`"olist_real"`) | Customer unique ID preserved; deterministic email generated (`olist.cust.{id}@example.com`) to enforce MongoDB unique email index constraint. Addresses formatted with Brazilian postal CEP. |
| `olist_orders_dataset.csv`<br>+ `olist_order_items_dataset.csv` | **`orders`**<br>- `_id` (`ObjectId`)<br>- `customer_id` (`ObjectId`, Ref)<br>- `items` (`Array` of Embedded Docs)<br>- `shipping_address` (`Embedded Subdoc`)<br>- `subtotal` (`Double`)<br>- `status` (`String`)<br>- `created_at` (`ISODate` UTC) | Relational order items de-normalized into embedded snapshot documents with unit price and line totals. Order status mapped to ShopSphere state machine (`delivered`, `shipped`, `confirmed`, `pending`, `cancelled`). |
| `olist_order_reviews_dataset.csv`<br>- `review_score` (1-5)<br>- `review_comment_message`<br>- `review_creation_date` | **`reviews`**<br>- `_id` (`ObjectId`)<br>- `product_id` (`ObjectId`, Ref)<br>- `customer_id` (`ObjectId`, Ref)<br>- `order_id` (`ObjectId`, Ref)<br>- `rating` (`Int32`, 1-5)<br>- `review_text` (`String`) | Real Portuguese customer review scores and feedback mapped. Triggers real-time recalculation of product `rating_average` and `review_count`. |
| *Synthesized from Orders* | **`inventory_movements`**<br>- `change_quantity`<br>- `reason`<br>- `source` (`"synthetic_olist_inventory"`) | Since Olist is a marketplace without warehouse inventory records, synthetic stock allocations and fulfillment movements are generated and tagged distinctly. |

---

## 📊 Database Collections & Schemas

### 1. `products`
```json
{
  "_id": ObjectId("..."),
  "name": "Apple Smart Ring Sleep and Heart Rate Tracker",
  "sku": "AUDI-APP-0028",
  "category": "Audio & Wearables",
  "brand": "Apple",
  "description": "Titanium smart ring with sleep analysis.",
  "price": 307.69,
  "stock_quantity": 42,
  "tags": ["audio", "wearables", "tech"],
  "rating_average": 4.5,
  "review_count": 8,
  "image_url": "https://images.unsplash.com/...",
  "created_at": ISODate("2026-06-15T10:00:00Z"),
  "updated_at": ISODate("2026-10-15T12:00:00Z")
}
```
**Indexes:** `{ sku: 1 }` (Unique), `{ category: 1, price: 1 }` (Compound), `{ name: "text" }`.

### 2. `customers`
```json
{
  "_id": ObjectId("..."),
  "name": "Sarah Connor",
  "email": "sarah.c@example.com",
  "phone": "+1-555-0199",
  "address": "404 Cyberdyne Way",
  "city": "Los Angeles",
  "created_at": ISODate("2026-05-10T08:30:00Z")
}
```
**Indexes:** `{ email: 1 }` (Unique), `{ city: 1 }`.

### 3. `orders`
```json
{
  "_id": ObjectId("..."),
  "customer_id": ObjectId("..."),
  "items": [
    {
      "product_id": ObjectId("..."),
      "product_name": "Apple Smart Ring...",
      "sku": "AUDI-APP-0028",
      "unit_price": 307.69,
      "quantity": 1,
      "line_total": 307.69
    }
  ],
  "shipping_address": {
    "street": "404 Cyberdyne Way",
    "city": "Los Angeles",
    "state": "CA",
    "postal_code": "90001",
    "country": "USA"
  },
  "subtotal": 307.69,
  "status": "delivered",
  "notes": "Leave at front desk",
  "created_at": ISODate("2026-09-12T14:22:00Z"),
  "updated_at": ISODate("2026-09-14T09:10:00Z")
}
```
**Indexes:** `{ customer_id: 1 }`, `{ status: 1, created_at: -1 }` (Compound).

### 4. `reviews`
```json
{
  "_id": ObjectId("..."),
  "product_id": ObjectId("..."),
  "customer_id": ObjectId("..."),
  "rating": 5,
  "review_text": "Exceptional battery life and accurate biometric data.",
  "created_at": ISODate("2026-09-15T18:00:00Z")
}
```
**Indexes:** `{ product_id: 1 }`, `{ customer_id: 1 }`.

### 5. `inventory_movements`
```json
{
  "_id": ObjectId("..."),
  "product_id": ObjectId("..."),
  "change_quantity": -1,
  "reason": "Order Fulfillment #ORD-6ad0c7",
  "related_order_id": ObjectId("..."),
  "created_at": ISODate("2026-09-12T14:22:01Z")
}
```
**Indexes:** `{ product_id: 1, created_at: -1 }` (Compound).

---

## 📡 REST API Endpoint Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Live MongoDB connection diagnostic & status |
| `GET` | `/api/v1/dashboard/summary` | Real-time aggregated executive metrics |
| `GET` | `/api/v1/products` | Paginated product list with search, sorting, and filters |
| `POST` | `/api/v1/products` | Create product (enforces unique SKU & `$jsonSchema`) |
| `GET` | `/api/v1/products/{id}` | Single product lookup by `ObjectId` |
| `PUT` | `/api/v1/products/{id}` | Update product details |
| `DELETE` | `/api/v1/products/{id}` | Delete product (with integrity check) |
| `GET` | `/api/v1/customers` | Customer list with total orders and lifetime spend |
| `POST` | `/api/v1/customers` | Register customer (unique email validation) |
| `GET` | `/api/v1/orders` | Paginated order history with status filters |
| `POST` | `/api/v1/orders` | Place order (atomic stock decrement & snapshot) |
| `POST` | `/api/v1/orders/{id}/cancel` | Cancel order (atomic stock restoration & audit entry) |
| `GET` | `/api/v1/inventory` | Inventory status & low-stock alerts |
| `POST` | `/api/v1/inventory/adjust` | Manual stock in/out adjustment with audit logging |
| `GET` | `/api/v1/reviews` | Review list with product rating distributions |
| `POST` | `/api/v1/reviews` | Create product review and recompute rating averages |
| `GET` | `/api/v1/analytics/overview` | Advanced business intelligence reports |
| `GET` | `/api/v1/analytics/export/csv` | Export analytics report as CSV |
| **CONCEPTS LAB** | | |
| `POST` | `/api/v1/concepts/crud-demo` | Interactive CRUD operations sandbox on demo collection |
| `POST` | `/api/v1/concepts/aggregate-demo`| Execute any of the 8 real aggregation pipelines |
| `POST` | `/api/v1/concepts/explain-demo` | Live `explain("executionStats")` comparing IXSCAN vs COLLSCAN |
| `POST` | `/api/v1/concepts/validation-demo`| Test database-level `$jsonSchema` rejection |
| `GET` | `/api/v1/concepts/indexes` | View all active indexes and their definitions |

---

## 🧪 Automated Testing

ShopSphere includes a comprehensive Pytest automated test suite in `backend/tests/test_api.py`.

To run the tests:
```powershell
cd d:\Mongo_db-project\ShopSphere\backend
.\venv\Scripts\Activate.ps1
pytest -v
```

### Verified Test Cases:
1. `test_product_crud_lifecycle`: Full product creation, read, update, and deletion.
2. `test_duplicate_sku_rejection`: Enforces unique MongoDB index on `products.sku` (HTTP 409).
3. `test_customer_email_uniqueness`: Enforces unique index on `customers.email`.
4. `test_order_creation_stock_decrement`: Verifies atomic stock deduction and line item snapshots.
5. `test_order_insufficient_stock_rejection`: Validates inventory safeguards against overselling.
6. `test_order_cancellation_stock_restoration`: Validates automatic inventory restoration upon cancellation.
7. `test_order_invalid_status_transition`: Prevents illegal state transitions (e.g., delivered $\rightarrow$ pending).
8. `test_aggregation_category_sales`: Validates `$unwind` + `$group` pipeline calculations.
9. `test_explain_query_optimization`: Asserts `IXSCAN` on indexed SKU vs `COLLSCAN` on description.
10. `test_schema_validation_rejection`: Tests MongoDB `$jsonSchema` engine rejecting non-compliant documents.

---

## 🎓 College Viva & Interview Guide

For detailed notes on MongoDB data modeling, B-Tree indexes, pipeline stages, and the top 25 viva questions with model answers, see:
👉 **[MongoDB Architecture & Viva Voce Guide](docs/mongodb-concepts.md)**

---

## 📝 License & Academic Honor Code
Built as an educational software engineering and database systems project. Free to use for study, portfolio presentations, and academic evaluation.
