"""
Generate publication-quality diagrams for ShopSphere Project Report.
Uses matplotlib to generate 300 DPI PNG diagrams with modern design aesthetics.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = r"D:\Mongo_db-project\ShopSphere\report_assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. System Architecture Diagram
# -----------------------------------------------------------------------------
def generate_system_architecture():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # Background
    fig.patch.set_facecolor("#f8fafc")
    ax.set_facecolor("#f8fafc")

    # Title
    ax.text(7, 8.5, "ShopSphere — Full-Stack System Architecture", ha="center", va="center",
            fontsize=18, fontweight="bold", color="#0f172a", fontfamily="sans-serif")
    ax.text(7, 8.15, "Three-Tier Client-Server Architecture on MongoDB Community 8.0",
            ha="center", va="center", fontsize=11, color="#64748b", fontfamily="sans-serif")

    # Layer 1: Frontend Client
    box_fe = patches.FancyBboxPatch((0.8, 5.8), 12.4, 1.8, boxstyle="round,pad=0.2,rounding_size=0.15",
                                    facecolor="#ffffff", edgecolor="#3b82f6", linewidth=2)
    ax.add_patch(box_fe)
    ax.text(1.2, 7.3, "PRESENTATION TIER — Web Browser Client (http://127.0.0.1:5173)",
            fontsize=11, fontweight="bold", color="#1d4ed8")
    
    # Submodules in frontend
    fe_modules = [
        ("Executive Dashboard", "Recharts Time-Series & Metrics", 1.2),
        ("Catalog Management", "Grid/Table, Filters & Search", 4.3),
        ("Customer & CRM", "LTV & Segment Analytics", 7.4),
        ("Concepts Lab", "Live CRUD, Aggregation & Explain", 10.5)
    ]
    for title, desc, x_pos in fe_modules:
        m_box = patches.FancyBboxPatch((x_pos, 6.0), 2.7, 1.0, boxstyle="round,pad=0.1",
                                       facecolor="#eff6ff", edgecolor="#bfdbfe", linewidth=1)
        ax.add_patch(m_box)
        ax.text(x_pos + 1.35, 6.65, title, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#1e3a8a")
        ax.text(x_pos + 1.35, 6.3, desc, ha="center", va="center", fontsize=7.5, color="#475569")

    # Arrow 1: Frontend <-> Backend
    ax.annotate("", xy=(7, 4.8), xytext=(7, 5.6),
                arrowprops=dict(arrowstyle="<->", color="#0284c7", lw=2.5, shrinkA=5, shrinkB=5))
    ax.text(7.2, 5.2, "RESTful JSON / Axios HTTP Client\n(CORS Enabled, OpenAPI 3.1)",
            fontsize=8.5, color="#0369a1", va="center", fontweight="semibold")

    # Layer 2: Backend Application Server
    box_be = patches.FancyBboxPatch((0.8, 3.2), 12.4, 1.5, boxstyle="round,pad=0.2,rounding_size=0.15",
                                    facecolor="#ffffff", edgecolor="#10b981", linewidth=2)
    ax.add_patch(box_be)
    ax.text(1.2, 4.4, "APPLICATION TIER — FastAPI Backend (http://127.0.0.1:8000, Python 3.12)",
            fontsize=11, fontweight="bold", color="#047857")

    be_modules = [
        ("Routers & Endpoints", "Dashboard, Products, Orders, Concepts", 1.2),
        ("Service Business Logic", "Stock Controls, Order Immutability", 4.3),
        ("Pydantic v2 Schemas", "Input Validation & BSON Serializers", 7.4),
        ("PyMongo 4.x Driver", "Connection Pool & Safe Transactions", 10.5)
    ]
    for title, desc, x_pos in be_modules:
        m_box = patches.FancyBboxPatch((x_pos, 3.4), 2.7, 0.75, boxstyle="round,pad=0.1",
                                       facecolor="#ecfdf5", edgecolor="#a7f3d0", linewidth=1)
        ax.add_patch(m_box)
        ax.text(x_pos + 1.35, 3.9, title, ha="center", va="center", fontsize=9, fontweight="bold", color="#065f46")
        ax.text(x_pos + 1.35, 3.6, desc, ha="center", va="center", fontsize=7.5, color="#475569")

    # Arrow 2: Backend <-> MongoDB
    ax.annotate("", xy=(7, 2.2), xytext=(7, 3.0),
                arrowprops=dict(arrowstyle="<->", color="#059669", lw=2.5, shrinkA=5, shrinkB=5))
    ax.text(7.2, 2.6, "PyMongo Wire Protocol (TCP 27017)\nBSON Document Operations & Aggregations",
            fontsize=8.5, color="#047857", va="center", fontweight="semibold")

    # Layer 3: Database Storage Tier
    box_db = patches.FancyBboxPatch((0.8, 0.4), 12.4, 1.7, boxstyle="round,pad=0.2,rounding_size=0.15",
                                    facecolor="#ffffff", edgecolor="#8b5cf6", linewidth=2)
    ax.add_patch(box_db)
    ax.text(1.2, 1.8, "PERSISTENCE TIER — MongoDB Community Server 8.0 (WiredTiger Storage Engine)",
            fontsize=11, fontweight="bold", color="#6d28d9")

    db_collections = [
        ("products", "32,951 docs", "Unique SKU, Category-Price Index", 1.1),
        ("customers", "99,441 docs", "Unique Email (Partial), City Index", 3.5),
        ("orders", "98,666 docs", "Embedded items, Status & Date Idx", 5.9),
        ("reviews", "97,709 docs", "Composite Key, Product_id Idx", 8.3),
        ("sellers / ledger", "3,095 sellers", "0 inventory_movements (Olist)", 10.7)
    ]
    for name, count, idx_info, x_pos in db_collections:
        c_box = patches.FancyBboxPatch((x_pos, 0.6), 2.2, 0.95, boxstyle="round,pad=0.08",
                                       facecolor="#f5f3ff", edgecolor="#ddd6fe", linewidth=1)
        ax.add_patch(c_box)
        ax.text(x_pos + 1.1, 1.3, name, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#4c1d95")
        ax.text(x_pos + 1.1, 1.0, count, ha="center", va="center", fontsize=8, fontweight="semibold", color="#5b21b6")
        ax.text(x_pos + 1.1, 0.75, idx_info, ha="center", va="center", fontsize=6.5, color="#6b7280")

    plt.tight_layout()
    out_file = os.path.join(OUTPUT_DIR, "architecture_diagram.png")
    plt.savefig(out_file, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print("Generated architecture_diagram.png")


# -----------------------------------------------------------------------------
# 2. Olist CSV to MongoDB Import Workflow Diagram
# -----------------------------------------------------------------------------
def generate_import_workflow():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    fig.patch.set_facecolor("#f8fafc")
    ax.set_facecolor("#f8fafc")

    ax.text(7, 7.5, "ShopSphere — Olist Brazilian E-Commerce Import Pipeline",
            ha="center", va="center", fontsize=17, fontweight="bold", color="#0f172a")
    ax.text(7, 7.15, "Automated Relational Normalization, Denormalization & Idempotent Ingestion",
            ha="center", va="center", fontsize=10.5, color="#64748b")

    # Step 1: Raw CSVs
    box_step1 = patches.FancyBboxPatch((0.6, 1.8), 2.6, 4.8, boxstyle="round,pad=0.15",
                                       facecolor="#ffffff", edgecolor="#f59e0b", linewidth=1.8)
    ax.add_patch(box_step1)
    ax.text(1.9, 6.2, "1. Raw Kaggle CSVs", ha="center", fontsize=11, fontweight="bold", color="#b45309")
    ax.text(1.9, 5.85, "(ShopSphere/data/olist/raw)", ha="center", fontsize=7.5, color="#78350f")

    csv_items = [
        "olist_products (32.9k)",
        "category_trans (71 rows)",
        "olist_customers (99.4k)",
        "olist_orders (99.4k)",
        "order_items (112.6k)",
        "order_payments (103.8k)",
        "order_reviews (99.2k)",
        "olist_sellers (3.0k)"
    ]
    for i, item in enumerate(csv_items):
        y = 5.3 - (i * 0.45)
        ax.text(1.9, y, item, ha="center", va="center", fontsize=8,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#fef3c7", edgecolor="#fde68a", lw=0.8))

    # Arrow 1 -> 2
    ax.annotate("", xy=(3.8, 4.2), xytext=(3.3, 4.2),
                arrowprops=dict(arrowstyle="->", color="#f59e0b", lw=2.5))

    # Step 2: Extraction & Sanitization
    box_step2 = patches.FancyBboxPatch((3.9, 2.2), 2.8, 4.0, boxstyle="round,pad=0.15",
                                       facecolor="#ffffff", edgecolor="#3b82f6", linewidth=1.8)
    ax.add_patch(box_step2)
    ax.text(5.3, 5.8, "2. Preprocessing & Cleaning", ha="center", fontsize=10.5, fontweight="bold", color="#1d4ed8")
    
    clean_tasks = [
        "UTF-8 BOM Header Stripping",
        "PT -> EN Category Translation",
        "Deterministic UUID5 ObjectIds",
        "Deterministic Clean SKUs",
        "Null Anonymized Customer Emails",
        "Partial Unique Index Alignment",
        "Timestamps Parsed to UTC Date"
    ]
    for i, t in enumerate(clean_tasks):
        y = 5.2 - (i * 0.45)
        ax.text(5.3, y, f"• {t}", ha="center", va="center", fontsize=8, color="#1e293b")

    # Arrow 2 -> 3
    ax.annotate("", xy=(7.3, 4.2), xytext=(6.8, 4.2),
                arrowprops=dict(arrowstyle="->", color="#3b82f6", lw=2.5))

    # Step 3: Transformation & Denormalization
    box_step3 = patches.FancyBboxPatch((7.4, 2.2), 2.8, 4.0, boxstyle="round,pad=0.15",
                                       facecolor="#ffffff", edgecolor="#8b5cf6", linewidth=1.8)
    ax.add_patch(box_step3)
    ax.text(8.8, 5.8, "3. Denormalization Engine", ha="center", fontsize=10.5, fontweight="bold", color="#6d28d9")

    denorm_tasks = [
        "In-Memory Items Grouping",
        "In-Memory Payments Grouping",
        "Embedded Line Items in Orders",
        "Embedded Shipping Address",
        "Skip 775 Orders with 0 Items",
        "($jsonSchema minItems: 1)",
        "Tagged is_historical = true",
        "Tagged source = 'olist_real'"
    ]
    for i, t in enumerate(denorm_tasks):
        y = 5.2 - (i * 0.45)
        color = "#b91c1c" if "Skip" in t else "#1e293b"
        fw = "bold" if "Skip" in t else "normal"
        ax.text(8.8, y, f"• {t}", ha="center", va="center", fontsize=8, color=color, fontweight=fw)

    # Arrow 3 -> 4
    ax.annotate("", xy=(10.8, 4.2), xytext=(10.3, 4.2),
                arrowprops=dict(arrowstyle="->", color="#8b5cf6", lw=2.5))

    # Step 4: MongoDB Bulk Upsert
    box_step4 = patches.FancyBboxPatch((10.9, 1.8), 2.5, 4.8, boxstyle="round,pad=0.15",
                                       facecolor="#ffffff", edgecolor="#10b981", linewidth=1.8)
    ax.add_patch(box_step4)
    ax.text(12.15, 6.2, "4. Idempotent Ingestion", ha="center", fontsize=10.5, fontweight="bold", color="#047857")
    ax.text(12.15, 5.85, "(db: shopsphere_olist)", ha="center", fontsize=7.5, color="#064e3b")

    mongo_results = [
        ("products", "32,951 docs"),
        ("customers", "99,441 docs"),
        ("orders", "98,666 docs"),
        ("reviews", "97,709 docs"),
        ("sellers", "3,095 docs"),
        ("inventory", "0 docs (clean)"),
        ("demo", "4 sample docs")
    ]
    for i, (col, cnt) in enumerate(mongo_results):
        y = 5.3 - (i * 0.5)
        ax.text(12.15, y, f"{col}\n{cnt}", ha="center", va="center", fontsize=8,
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#ecfdf5", edgecolor="#a7f3d0", lw=0.8),
                fontweight="semibold", color="#065f46")

    # Bottom summary banner
    summary_box = patches.FancyBboxPatch((0.6, 0.5), 12.8, 0.9, boxstyle="round,pad=0.15",
                                        facecolor="#f1f5f9", edgecolor="#cbd5e1", linewidth=1)
    ax.add_patch(summary_box)
    ax.text(7, 1.05, "Idempotency Guarantee: Repeated runs perform update_one(..., upsert=True) on external_id keys without duplicating data.",
            ha="center", va="center", fontsize=8.5, fontweight="bold", color="#1e293b")
    ax.text(7, 0.75, "Integrity Guarantee: Historical records marked immutable. Zero invented stock or synthetic contact info injected.",
            ha="center", va="center", fontsize=8, color="#475569")

    plt.tight_layout()
    out_file = os.path.join(OUTPUT_DIR, "import_workflow.png")
    plt.savefig(out_file, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print("Generated import_workflow.png")


# -----------------------------------------------------------------------------
# 3. Database Data Model Diagram (Embedded vs Referenced)
# -----------------------------------------------------------------------------
def generate_database_model():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    fig.patch.set_facecolor("#f8fafc")
    ax.set_facecolor("#f8fafc")

    ax.text(8.0, 8.6, "ShopSphere — MongoDB Document Model & Schema Relationships",
            ha="center", va="center", fontsize=18, fontweight="bold", color="#0f172a")
    ax.text(8.0, 8.25, "Hybrid NoSQL Design: Embedded 1-to-Few Arrays & Referenced ObjectIds",
            ha="center", va="center", fontsize=11, color="#64748b")

    # Collection 1: Customers (Left)
    c_box = patches.FancyBboxPatch((0.5, 4.3), 3.6, 3.5, boxstyle="round,pad=0.15",
                                   facecolor="#ffffff", edgecolor="#3b82f6", linewidth=2)
    ax.add_patch(c_box)
    ax.text(2.3, 7.5, "customers", ha="center", fontsize=13, fontweight="bold", color="#1d4ed8")
    ax.text(2.3, 7.15, "Count: 99,441 documents", ha="center", fontsize=8.5, color="#64748b")
    
    c_fields = [
        ("_id", "ObjectId", "PK (UUID5 hash)"),
        ("external_id", "String", "Olist customer_id"),
        ("external_unique_id", "String", "Unique buyer identifier"),
        ("name", "String", "Brazilian customer tag"),
        ("email", "String / null", "Partial Unique Index"),
        ("city", "String", "Indexed: {city: 1}"),
        ("state", "String", "Brazilian 2-letter state"),
        ("source", "String", "'olist_real' | 'demo'")
    ]
    for i, (fname, ftype, note) in enumerate(c_fields):
        y = 6.7 - (i * 0.35)
        ax.text(0.7, y, fname, fontsize=8.5, fontweight="bold", color="#0f172a")
        ax.text(2.1, y, ftype, fontsize=8, color="#0284c7")
        ax.text(2.8, y, note, fontsize=7.5, color="#64748b")

    # Collection 2: Orders (Center) - The core embedded document
    o_box = patches.FancyBboxPatch((5.3, 1.8), 5.2, 6.0, boxstyle="round,pad=0.15",
                                   facecolor="#ffffff", edgecolor="#10b981", linewidth=2)
    ax.add_patch(o_box)
    ax.text(7.9, 7.5, "orders (Core Aggregate)", ha="center", fontsize=13, fontweight="bold", color="#047857")
    ax.text(7.9, 7.15, "Count: 98,666 docs ($jsonSchema validated)", ha="center", fontsize=8.5, color="#64748b")

    o_fields = [
        ("_id", "ObjectId", "PK (UUID5 hash)"),
        ("external_id", "String", "Unique Index"),
        ("customer_id", "ObjectId", "FK -> customers._id"),
        ("[EMBEDDED] items", "Array", "Line Item Snapshots:"),
        ("  • product_id", "ObjectId", "FK -> products._id"),
        ("  • product_name", "String", "Historical catalog name"),
        ("  • sku", "String", "Historical SKU snapshot"),
        ("  • unit_price", "Double", "Locked purchase price"),
        ("  • quantity", "Int32", "Units purchased"),
        ("  • line_total", "Double", "unit_price * quantity"),
        ("[EMBEDDED] shipping_addr", "Subdoc", "Street, City, State, CEP"),
        ("[EMBEDDED] payments", "Array", "Installments, Type, Value"),
        ("subtotal / total_amount", "Double", "Order monetary sums"),
        ("status", "Enum", "delivered, shipped, pending..."),
        ("is_historical", "Boolean", "true -> Immutable"),
        ("created_at", "ISODate", "Compound Idx: {status, date}")
    ]
    for i, (fname, ftype, note) in enumerate(o_fields):
        y = 6.75 - (i * 0.28)
        color = "#047857" if "EMBEDDED" in fname else ("#0f172a" if not fname.startswith(" ") else "#334155")
        fw = "bold" if ("EMBEDDED" in fname or fname in ["_id", "customer_id", "status"]) else "normal"
        ax.text(5.5, y, fname, fontsize=8, fontweight=fw, color=color)
        ax.text(7.7, y, ftype, fontsize=7.5, color="#059669")
        ax.text(8.7, y, note, fontsize=7.5, color="#64748b")

    # Collection 3: Products (Right)
    p_box = patches.FancyBboxPatch((11.7, 4.3), 3.8, 3.5, boxstyle="round,pad=0.15",
                                   facecolor="#ffffff", edgecolor="#8b5cf6", linewidth=2)
    ax.add_patch(p_box)
    ax.text(13.6, 7.5, "products", ha="center", fontsize=13, fontweight="bold", color="#6d28d9")
    ax.text(13.6, 7.15, "Count: 32,951 documents", ha="center", fontsize=8.5, color="#64748b")

    p_fields = [
        ("_id", "ObjectId", "PK (UUID5 hash)"),
        ("sku", "String", "Unique B-Tree Index"),
        ("name", "String", "Text Index for Search"),
        ("category", "String", "Compound: {category, price}"),
        ("price", "Double", "Validator minimum: 0.01"),
        ("stock_quantity", "Int32", "0 for Olist (untracked)"),
        ("rating_average", "Double", "Computed from reviews"),
        ("review_count", "Int32", "Recalculated count")
    ]
    for i, (fname, ftype, note) in enumerate(p_fields):
        y = 6.7 - (i * 0.35)
        ax.text(11.9, y, fname, fontsize=8.5, fontweight="bold", color="#0f172a")
        ax.text(13.2, y, ftype, fontsize=8, color="#7c3aed")
        ax.text(13.9, y, note, fontsize=7.5, color="#64748b")

    # Collection 4: Reviews (Bottom Left)
    r_box = patches.FancyBboxPatch((0.5, 0.6), 3.6, 3.2, boxstyle="round,pad=0.15",
                                   facecolor="#ffffff", edgecolor="#f59e0b", linewidth=1.8)
    ax.add_patch(r_box)
    ax.text(2.3, 3.4, "reviews", ha="center", fontsize=12, fontweight="bold", color="#b45309")
    ax.text(2.3, 3.1, "Count: 97,709 documents", ha="center", fontsize=8, color="#64748b")

    r_fields = [
        ("_id", "ObjectId", "PK (Deterministic)"),
        ("product_id", "ObjectId", "FK -> products._id"),
        ("customer_id", "ObjectId", "FK -> customers._id"),
        ("order_id", "ObjectId", "FK -> orders._id"),
        ("rating", "Int32", "1 to 5 star rating"),
        ("review_text", "String", "Portuguese feedback"),
        ("created_at", "ISODate", "Descending index")
    ]
    for i, (fname, ftype, note) in enumerate(r_fields):
        y = 2.75 - (i * 0.32)
        ax.text(0.7, y, fname, fontsize=8, fontweight="bold", color="#0f172a")
        ax.text(1.9, y, ftype, fontsize=7.5, color="#d97706")
        ax.text(2.6, y, note, fontsize=7, color="#64748b")

    # Collection 5: Inventory Movements (Bottom Right)
    inv_box = patches.FancyBboxPatch((11.7, 0.6), 3.8, 3.2, boxstyle="round,pad=0.15",
                                     facecolor="#ffffff", edgecolor="#ec4899", linewidth=1.8)
    ax.add_patch(inv_box)
    ax.text(13.6, 3.4, "inventory_movements", ha="center", fontsize=12, fontweight="bold", color="#be185d")
    ax.text(13.6, 3.1, "Count: 0 (Olist) / Operational Ledger", ha="center", fontsize=8, color="#64748b")

    inv_fields = [
        ("_id", "ObjectId", "PK"),
        ("product_id", "ObjectId", "FK -> products._id"),
        ("change_quantity", "Int32", "+/- stock adjustment"),
        ("reason", "String", "Fulfillment, Restock, Return"),
        ("related_order_id", "ObjectId", "Optional FK -> orders"),
        ("created_at", "ISODate", "Compound: {product_id, date}")
    ]
    for i, (fname, ftype, note) in enumerate(inv_fields):
        y = 2.75 - (i * 0.32)
        ax.text(11.9, y, fname, fontsize=8, fontweight="bold", color="#0f172a")
        ax.text(13.4, y, ftype, fontsize=7.5, color="#db2777")
        ax.text(14.1, y, note, fontsize=7, color="#64748b")

    # Relationship Arrows
    # Customer -> Orders (1:N Reference)
    ax.annotate("", xy=(5.25, 6.0), xytext=(4.15, 6.0),
                arrowprops=dict(arrowstyle="->", color="#3b82f6", lw=2.5))
    ax.text(4.7, 6.25, "1:N Ref\n(customer_id)", fontsize=8, fontweight="bold", color="#1d4ed8", va="bottom", ha="center")

    # Orders -> Products (Items Reference)
    ax.annotate("", xy=(11.65, 6.0), xytext=(10.55, 6.0),
                arrowprops=dict(arrowstyle="->", color="#8b5cf6", lw=2.5))
    ax.text(11.1, 6.25, "Embedded Snapshot\n+ Product FK", fontsize=8, fontweight="bold", color="#6d28d9", va="bottom", ha="center")

    # Reviews -> Products (Clean bottom curve)
    ax.annotate("", xy=(11.65, 5.0), xytext=(4.15, 2.0),
                arrowprops=dict(arrowstyle="->", color="#f59e0b", lw=2, ls="--",
                                connectionstyle="angle,angleA=0,angleB=90,rad=10"))
    ax.text(7.9, 1.1, "reviews.product_id -> products._id (Rating Aggregation FK)",
            fontsize=8.5, fontweight="bold", color="#b45309", ha="center",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#fffbeb", edgecolor="#fde68a", lw=1))

    # Inventory -> Products
    ax.annotate("", xy=(13.6, 4.25), xytext=(13.6, 3.85),
                arrowprops=dict(arrowstyle="->", color="#ec4899", lw=2))
    ax.text(14.3, 4.05, "product_id FK", fontsize=7.5, color="#be185d", va="center")

    plt.tight_layout()
    out_file = os.path.join(OUTPUT_DIR, "database_model.png")
    plt.savefig(out_file, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print("Generated database_model.png")


# -----------------------------------------------------------------------------
# 4. API Request Flow Diagram
# -----------------------------------------------------------------------------
def generate_api_request_flow():
    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis("off")

    fig.patch.set_facecolor("#f8fafc")
    ax.set_facecolor("#f8fafc")

    ax.text(7, 6.5, "ShopSphere — End-to-End API Request & Query Pipeline",
            ha="center", va="center", fontsize=17, fontweight="bold", color="#0f172a")
    ax.text(7, 6.15, "Layered Architecture: Client -> FastRouter -> Schema Validator -> Service -> Repository -> MongoDB",
            ha="center", va="center", fontsize=10.5, color="#64748b")

    stages = [
        ("1. React Client", "Axios HTTP Call\nJSON Request Payload\nBearer/Demo Headers", "#3b82f6", 1.5),
        ("2. FastAPI Router", "Path & Query Parsing\nRoute Decorators\nDependency Injection", "#0284c7", 4.2),
        ("3. Service Logic", "Stock Controls\nHistorical Immutability\nTwo-Phase Fallback", "#059669", 6.9),
        ("4. PyMongo Repo", "Aggregation Pipelines\nexplain('executionStats')\nB-Tree Index Scans", "#8b5cf6", 9.6),
        ("5. MongoDB 8.0", "WiredTiger Engine\n$jsonSchema Validation\nDocument Persistence", "#047857", 12.3)
    ]

    for title, desc, col, x_pos in stages:
        box = patches.FancyBboxPatch((x_pos - 1.1, 2.4), 2.2, 3.0, boxstyle="round,pad=0.15",
                                     facecolor="#ffffff", edgecolor=col, linewidth=2)
        ax.add_patch(box)
        ax.text(x_pos, 5.0, title, ha="center", fontsize=10, fontweight="bold", color=col)
        ax.text(x_pos, 3.8, desc, ha="center", fontsize=8, color="#334155")

    # Arrows between boxes
    for x in [2.7, 5.4, 8.1, 10.8]:
        ax.annotate("", xy=(x + 0.35, 4.2), xytext=(x - 0.05, 4.2),
                    arrowprops=dict(arrowstyle="->", color="#64748b", lw=2.5))
        ax.annotate("", xy=(x - 0.05, 3.6), xytext=(x + 0.35, 3.6),
                    arrowprops=dict(arrowstyle="->", color="#94a3b8", lw=2, ls="--"))

    ax.text(7, 1.6, "Request Flow (Solid Arrow) -> / <- Response Flow (Dashed Arrow)",
            ha="center", fontsize=9.5, fontweight="bold", color="#334155")
    ax.text(7, 1.2, "Includes automatic BSON ObjectId serialization and standard HTTP status codes (200, 201, 400, 404, 409, 422)",
            ha="center", fontsize=8.5, color="#64748b")

    plt.tight_layout()
    out_file = os.path.join(OUTPUT_DIR, "api_request_flow.png")
    plt.savefig(out_file, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print("Generated api_request_flow.png")


# -----------------------------------------------------------------------------
# 5. Database Isolation Diagram
# -----------------------------------------------------------------------------
def generate_data_isolation():
    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis("off")

    fig.patch.set_facecolor("#f8fafc")
    ax.set_facecolor("#f8fafc")

    ax.text(7, 6.5, "ShopSphere — Multi-Database Isolation Architecture",
            ha="center", va="center", fontsize=17, fontweight="bold", color="#0f172a")
    ax.text(7, 6.15, "Total Namespace Separation for Historical Integrity, Live Demos, and Automated Testing",
            ha="center", va="center", fontsize=10.5, color="#64748b")

    dbs = [
        ("shopsphere_olist", "Primary Historical Dataset",
         ["• 99,441 Customers, 98,666 Orders",
          "• 32,951 Products, 97,709 Reviews",
          "• Tagged: source='olist_real'",
          "• Tagged: is_historical=true",
          "• Strict Immutability Guard: HTTP 400",
          "• Clean inventory_movements (0 docs)"],
         "#3b82f6", 2.6),
        ("shopsphere", "Operational Demo Sandbox",
         ["• 56 Customers, 226 Orders",
          "• 120 Products, 130 Reviews",
          "• 550 Inventory Movements",
          "• 40 shopsphere_demo records",
          "• Active Stock Decrement & Restore",
          "• Modifiable Demo Catalog"],
         "#10b981", 7.0),
        ("shopsphere_test", "Pytest CI/CD Isolation",
         ["• 100% Dynamic Fixture Lifecycle",
          "• Created on test setup",
          "• Dropped/Cleaned on teardown",
          "• 12 Automated Unit & Integration Tests",
          "• Zero side-effects on real datasets",
          "• Fast execution (0.69 seconds)"],
         "#8b5cf6", 11.4)
    ]

    for db_name, subtitle, bullets, col, x_pos in dbs:
        box = patches.FancyBboxPatch((x_pos - 1.8, 1.5), 3.6, 4.2, boxstyle="round,pad=0.15",
                                     facecolor="#ffffff", edgecolor=col, linewidth=2)
        ax.add_patch(box)
        ax.text(x_pos, 5.3, db_name, ha="center", fontsize=12, fontweight="bold", color=col)
        ax.text(x_pos, 4.95, subtitle, ha="center", fontsize=8.5, color="#64748b")
        for i, b in enumerate(bullets):
            y = 4.4 - (i * 0.45)
            ax.text(x_pos - 1.5, y, b, fontsize=8, color="#1e293b")

    ax.text(7, 0.9, "Isolation Safeguard: The application configuration (DATABASE_NAME in .env) switches targets seamlessly without cross-database pollution.",
            ha="center", fontsize=8.5, fontweight="bold", color="#334155")

    plt.tight_layout()
    out_file = os.path.join(OUTPUT_DIR, "data_isolation_diagram.png")
    plt.savefig(out_file, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print("Generated data_isolation_diagram.png")


if __name__ == "__main__":
    generate_system_architecture()
    generate_import_workflow()
    generate_database_model()
    generate_api_request_flow()
    generate_data_isolation()
    print("All diagrams generated successfully!")
