# Olist Brazilian E-Commerce Dataset Directory

Place the extracted CSV files from the Kaggle Olist Brazilian E-Commerce dataset here.

Dataset URL:
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

### Expected CSV Files in this directory:
1. `olist_products_dataset.csv`
2. `product_category_name_translation.csv`
3. `olist_customers_dataset.csv`
4. `olist_orders_dataset.csv`
5. `olist_order_items_dataset.csv`
6. `olist_order_reviews_dataset.csv`
7. (Optional) `olist_order_payments_dataset.csv`
8. (Optional) `olist_sellers_dataset.csv`
9. (Optional) `olist_geolocation_dataset.csv`

### Running the Importer:
Once the CSV files are copied into this folder, run:
```powershell
cd d:\Mongo_db-project\ShopSphere\backend
.\venv\Scripts\Activate.ps1
python scripts/import_dataset.py --limit-orders 1000
```
Use `--help` to see all available arguments (batch sizes, limits, drop/append mode, etc.).
