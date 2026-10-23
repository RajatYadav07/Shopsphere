# ShopSphere: Final Capstone Project Report Deliverables

**Institution:** Lovely Professional University (LPU), Punjab, India  
**School:** School of Computer Science and Engineering  
**Department:** Department of Computer Science and Engineering  
**Programme:** Bachelor of Technology in Computer Science and Engineering (B.Tech CSE)  
**Academic Session:** 2026–2027  
**Student Name:** RAJAT YADAV  
**Registration Number:** 12308041  
**Project Title:** ShopSphere — E-Commerce Database and Analytics System Using MongoDB  
**Project Guide / Faculty Name:** `[TO BE FILLED IN AFTER CONFIRMATION]`  

---

## 📂 Deliverables Summary

| File / Folder Path | Type | Size / Pages | Description |
| :--- | :--- | :--- | :--- |
| [`report/ShopSphere_MongoDB_Project_Report_Rajat_Yadav.docx`](report/ShopSphere_MongoDB_Project_Report_Rajat_Yadav.docx) | Microsoft Word (.docx) | **~2.90 MB** | Complete editable academic report formatted to LPU standards with all 25 sections, custom styles, tables, code listings, and 16 embedded figures. |
| [`report/ShopSphere_MongoDB_Project_Report_Rajat_Yadav.pdf`](report/ShopSphere_MongoDB_Project_Report_Rajat_Yadav.pdf) | Adobe PDF (.pdf) | **~1.90 MB (57 Pages)** | High-fidelity publication PDF exported directly via Microsoft Word COM engine with rendered fields, page numbers, and vector-rendered tables. |
| [`report_assets/`](report_assets/) | Directory | 16 High-Res Assets | Directory containing all 5 publication-quality architecture diagrams (300 DPI) and 11 authentic application/API screenshots. |
| [`README_Report.md`](README_Report.md) | Markdown | Documentation | Comprehensive documentation and verification summary of the generated report deliverables. |

---

## 🏛️ Report Structure — All 25 Required Sections Verified

The generated document preserves the academic order specified by Lovely Professional University:

1. **Title Page** — Official LPU capstone title page with student registration details, degree award text, and guide placeholder.
2. **Certificate** — Formal institutional certificate with unfilled signatures, designation, and department approval lines.
3. **Declaration** — Academic integrity and anti-plagiarism declaration by Rajat Yadav.
4. **Acknowledgement** — Academic acknowledgements to LPU faculty, department leadership, open-source communities, and Olist.
5. **Abstract** — 350-word structured academic abstract covering problem, architecture, hybrid NoSQL modeling, aggregations, query optimization, and validation.
6. **Table of Contents** — Comprehensive table of contents mapping sections and subsections with page references.
7. **List of Figures** — Complete numbered index of all 16 figures embedded in the document.
8. **List of Tables** — Complete numbered index of all 9 analytical and comparative tables.
9. **1. Introduction** — E-commerce database background, relational vs document paradigm, MongoDB 8.0 rationale, and ShopSphere overview.
10. **2. Problem Statement** — Relational join bottlenecks, historical consistency vs redundancy, real-time analytical demands, and data hygiene challenges.
11. **3. Objectives of the Project** — Primary aims and 7 concrete technical deliverables (modeling, CRUD, aggregations, indexing, `$jsonSchema`, ETL, isolation).
12. **4. Scope of the Project** — Detailed breakdown of 9 implemented functional modules and explicit limitations (no synthetic inventory, null emails, standalone transaction fallback).
13. **5. Literature Review** — Theoretical analysis of CAP theorem, NoSQL document stores, MongoDB WiredTiger storage engine (concurrency, caching, Snappy), FastAPI ASGI, React 18, and Olist dataset literature.
14. **6. System Requirements (Hardware and Software)** — Development vs production hardware specifications, complete verified software dependency stack, and network loopback topology.
15. **7. System Design and Architecture** — Three-tier architecture, component decomposition, ETL import pipeline workflow, API request lifecycle, and multi-database isolation.
16. **8. Database Design** — Collection schemas, hybrid embedding vs referencing rationale, sample BSON documents, collection-level `$jsonSchema` validators, and B-Tree indexing strategy.
17. **9. Implementation and Methodology** — Olist data discovery, UTF-8 BOM sanitization, Portuguese-to-English translation, deterministic UUID5 ObjectIds, idempotent bulk upserts, and service/repository implementation.
18. **10. MongoDB Queries and Operations** — Runnable CRUD operations, 8 production aggregation pipelines with code and explanations, empirical `explain("executionStats")` optimization benchmarks, and schema validation write rejection.
19. **11. Results and Output Screenshots** — Academic walkthrough of all 11 real application screenshots (Dashboard, Products, CRM, Orders, Reviews, Inventory, Analytics, Concepts Lab, Settings, Storefront, Swagger UI).
20. **12. Testing and Validation** — Automated testing strategy, 12 passing Pytest unit/integration tests (0.69s), comprehensive test matrix, frontend production build (2.22s), historical immutability validation, and idempotency matrix.
21. **13. Challenges Faced** — Ingestion hurdles (UTF-8 BOM, translations), handling null customer emails in unique indexes via partial filter expressions, relational-to-document denormalization, standalone transaction concurrency, and query optimization.
22. **14. Conclusion** — Summary of technical achievements, synthesis of theoretical principles with real big data, and pedagogical reflections.
23. **15. Future Scope** — 3-node Replica Sets, distributed sharding, MongoDB Atlas Vector Search, Change Streams event architectures, and JWT/RBAC security hardening.
24. **16. References / Bibliography** — Formal academic citations with official URLs (MongoDB Inc., Olist/Kaggle, FastAPI, React, academic papers).
25. **17. Appendix** — Appendix A (MongoDB shell commands), Appendix B (Data Dictionary), Appendix C (Setup Guide), and Appendix D (Top 15 Academic Viva Questions and Answers).

---

## 📊 Verified Live Database & System State

The report was verified against the active, live MongoDB Community Server 8.0 instance running locally on Windows:

- **MongoDB Server Version:** `8.0.34` (WiredTiger Storage Engine)
- **Primary Database:** `shopsphere_olist`
- **Verified Collection Document Counts:**
  - `products`: **32,951** documents
  - `customers`: **99,441** documents
  - `orders`: **98,666** documents (775 skipped due to 0 line items in raw data)
  - `reviews`: **97,709** documents
  - `sellers`: **3,095** documents
  - `inventory_movements`: **0** documents (Clean historical ledger; Olist marketplace does not provide warehouse ledgers)
  - `shopsphere_demo`: **4** documents (Isolated sandbox collection)
- **Demo Sandbox Database (`shopsphere`):** Preserved separately (120 products, 56 customers, 226 orders, 550 inventory movements).
- **Automated Test Database (`shopsphere_test`):** 100% isolated; dynamically initialized and dropped during test fixtures.

---

## 🧪 Verified Automated Testing & Build Results

### 1. Backend Pytest Suite
```powershell
cd D:\Mongo_db-project\ShopSphere\backend
.\venv\Scripts\Activate.ps1
pytest -v
```
**Outcome:** **12 passed** in **0.69s** against isolated `shopsphere_test`.
- `tests/test_analytics.py`: Dashboard summary and analytics overview with CSV export.
- `tests/test_concepts.py`: CRUD demo, aggregation playground, explain query plan, and schema validation rejections.
- `tests/test_customers.py`: Customer CRUD and partial unique email constraint.
- `tests/test_import_dataset.py`: File existence verification and end-to-end ETL import pipeline.
- `tests/test_orders.py`: Order placement, atomic stock decrement, and order cancellation stock restoration.
- `tests/test_products.py`: Server-side cursor pagination, product CRUD, and duplicate SKU rejection (HTTP 409).

### 2. Frontend Production Build
```powershell
cd D:\Mongo_db-project\ShopSphere\frontend
npm run build
```
**Outcome:** **Built successfully in 2.22s** (`tsc -b && vite build`) with zero TypeScript errors.

---

## 🖼️ Catalog of Embedded Figures

All figures embedded in the final report are stored in [`report_assets/`](report_assets/):

1. **`architecture_diagram.png`** (Figure 1): 300 DPI system architecture diagram illustrating the Presentation Tier (React + Vite), Application Tier (FastAPI), and Persistence Tier (MongoDB 8.0).
2. **`import_workflow.png`** (Figure 2): Detailed ETL pipeline diagram showing raw Olist CSV discovery, UTF-8 BOM cleaning, Portuguese translation, UUID5 hashing, denormalization, and idempotent upserts.
3. **`api_request_flow.png`** (Figure 3): End-to-end request lifecycle diagram tracing requests through FastAPI routers, Pydantic schemas, service logic, PyMongo repositories, and WiredTiger storage.
4. **`data_isolation_diagram.png`** (Figure 4): Multi-database namespace architecture diagram showing total separation between `shopsphere_olist`, `shopsphere`, and `shopsphere_test`.
5. **`database_model.png`** (Figure 5): Entity-relationship and document schema diagram illustrating embedded 1-to-few arrays (items, payments, shipping) vs referenced ObjectIds (customers, products, reviews).
6. **`dashboard.png`** (Figure 6): Real application screenshot of the Executive Performance Hub displaying $13.49M revenue, 98,199 orders, monthly revenue trends, and category shares.
7. **`products.png`** (Figure 7): Real application screenshot of the Product Catalogue management grid with search, category filtering, SKU badges, and price ranges.
8. **`customers.png`** (Figure 8): Real application screenshot of Customer CRM accounts displaying Brazilian state locations (SP, MG, RJ) and aggregated Lifetime Value (LTV).
9. **`orders.png`** (Figure 9): Real application screenshot of the Order Management ledger displaying embedded line-item counts, delivery statuses, and immutable Olist badges.
10. **`reviews.png`** (Figure 10): Real application screenshot of Customer Reviews displaying authentic Portuguese feedback and 1-to-5 star ratings.
11. **`inventory.png`** (Figure 11): Real application screenshot of the Inventory & Movement Audit ledger displaying warehouse stock balances and audit event logs.
12. **`analytics.png`** (Figure 12): Real application screenshot of Business Intelligence reports displaying revenue growth time series, order lifecycle breakdown, and sentiment analysis.
13. **`concepts_lab.png`** (Figure 13): Real application screenshot of the Interactive MongoDB Concepts Lab showing live CRUD execution, shell syntax, and BSON outputs.
14. **`settings.png`** (Figure 14): Real application screenshot of Database Settings displaying MongoDB 8.0.34 engine status, single topology, and collection volumes.
15. **`storefront.png`** (Figure 15): Real application screenshot of the Customer Storefront with interactive category pills, shopping bag, and product cards.
16. **`swagger_docs.png`** (Figure 16): Real screenshot of FastAPI interactive OpenAPI Swagger documentation at `http://127.0.0.1:8000/docs`.

---

## 🛠️ Instructions for Re-Generating or Re-Exporting

If any text or data is modified in the future, the deliverables can be regenerated with a single command:

### Re-Generate DOCX Report:
```powershell
& 'D:\Mongo_db-project\ShopSphere\backend\venv\Scripts\python.exe' 'D:\Mongo_db-project\ShopSphere\backend\scripts\generate_full_report.py'
```

### Re-Export to PDF via Word COM Automation:
```powershell
powershell -ExecutionPolicy Bypass -File "D:\Mongo_db-project\ShopSphere\backend\scripts\convert_docx_to_pdf.ps1" -docxPath "D:\Mongo_db-project\ShopSphere\report\ShopSphere_MongoDB_Project_Report_Rajat_Yadav.docx" -pdfPath "D:\Mongo_db-project\ShopSphere\report\ShopSphere_MongoDB_Project_Report_Rajat_Yadav.pdf"
```

---

## 📜 Dataset Attribution & Academic License

- **Dataset Source:** [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- **License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International ([CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/))
- **Ethical Compliance:** The dataset consists of anonymized historical transactions. No personal phone numbers or unprovided emails are generated; customer emails are maintained as `null` with partial unique index enforcement. All historical records are strictly immutable.
