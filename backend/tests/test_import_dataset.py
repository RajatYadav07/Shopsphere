import os
import csv
import tempfile
import pytest
from app.core.database import db_manager
from scripts.import_dataset import run_import, verify_dataset_files

def test_verify_dataset_files_missing():
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Empty directory should fail validation
        assert verify_dataset_files(tmp_dir) is False

def test_olist_import_pipeline_end_to_end():
    db = db_manager.get_database()
    assert db.name == "shopsphere_test", "Safety check: must run against isolated test database!"

    with tempfile.TemporaryDirectory() as tmp_dir:
        # 1. product_category_name_translation.csv
        with open(os.path.join(tmp_dir, "product_category_name_translation.csv"), "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["product_category_name", "product_category_name_english"])
            writer.writerow(["relogios_presentes", "watches_gifts"])
            writer.writerow(["beleza_saude", "health_beauty"])

        # 2. olist_products_dataset.csv
        with open(os.path.join(tmp_dir, "olist_products_dataset.csv"), "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["product_id", "product_category_name", "product_name_lenght", "product_description_lenght", "product_photos_qty", "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"])
            writer.writerow(["p1001", "relogios_presentes", "40", "150", "2", "350", "15", "10", "12"])
            writer.writerow(["p1002", "beleza_saude", "35", "120", "1", "200", "10", "8", "8"])

        # 3. olist_customers_dataset.csv
        with open(os.path.join(tmp_dir, "olist_customers_dataset.csv"), "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["customer_id", "customer_unique_id", "customer_zip_code_prefix", "customer_city", "customer_state"])
            writer.writerow(["c2001", "u9001", "01310", "sao paulo", "SP"])

        # 4. olist_order_items_dataset.csv
        with open(os.path.join(tmp_dir, "olist_order_items_dataset.csv"), "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["order_id", "order_item_id", "product_id", "seller_id", "shipping_limit_date", "price", "freight_value"])
            writer.writerow(["ord3001", "1", "p1001", "s501", "2026-02-01 12:00:00", "129.90", "15.00"])
            writer.writerow(["ord3001", "2", "p1002", "s502", "2026-02-01 12:00:00", "49.50", "10.00"])

        # 5. olist_orders_dataset.csv
        with open(os.path.join(tmp_dir, "olist_orders_dataset.csv"), "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["order_id", "customer_id", "order_status", "order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"])
            writer.writerow(["ord3001", "c2001", "delivered", "2026-01-15 10:30:00", "2026-01-15 11:00:00", "2026-01-16 14:00:00", "2026-01-20 16:00:00", "2026-01-25 00:00:00"])

        # 6. olist_order_reviews_dataset.csv
        with open(os.path.join(tmp_dir, "olist_order_reviews_dataset.csv"), "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["review_id", "order_id", "review_score", "review_comment_title", "review_comment_message", "review_creation_date", "review_answer_timestamp"])
            writer.writerow(["rev4001", "ord3001", "5", "Excelente", "Produto de altissima qualidade, chegou antes do prazo.", "2026-01-21 00:00:00", "2026-01-22 10:00:00"])

        # 7. olist_order_payments_dataset.csv
        with open(os.path.join(tmp_dir, "olist_order_payments_dataset.csv"), "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["order_id", "payment_sequential", "payment_type", "payment_installments", "payment_value"])
            writer.writerow(["ord3001", "1", "credit_card", "3", "194.40"])

        # 8. olist_sellers_dataset.csv
        with open(os.path.join(tmp_dir, "olist_sellers_dataset.csv"), "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["seller_id", "seller_zip_code_prefix", "seller_city", "seller_state"])
            writer.writerow(["s501", "13023", "campinas", "SP"])

        # Clean any preexisting test records
        db.products.delete_many({"external_id": {"$in": ["p1001", "p1002"]}})
        db.customers.delete_many({"external_id": "c2001"})
        db.orders.delete_many({"external_id": "ord3001"})
        db.reviews.delete_many({"external_id": "rev4001"})
        db.sellers.delete_many({"external_id": "s501"})

        # Run import pass 1
        success = run_import(
            data_dir=tmp_dir,
            db_name=db.name,
            limit_orders=10,
            limit_products=10,
            clear_existing_olist=False,
            synthetic_inventory=False
        )
        assert success is True

        # Test idempotency: Run import pass 2
        success_idempotent = run_import(
            data_dir=tmp_dir,
            db_name=db.name,
            limit_orders=10,
            limit_products=10,
            clear_existing_olist=False,
            synthetic_inventory=False
        )
        assert success_idempotent is True

        # Verify Product Ingestion & Category Translation
        prod1 = db.products.find_one({"external_id": "p1001"})
        assert prod1 is not None
        assert prod1["source"] == "olist_real"
        assert prod1["category"] == "Watches & Gifts"
        assert prod1["price"] == 129.90
        assert prod1["stock_quantity"] == 0
        assert prod1["inventory_tracked"] is False
        assert prod1["sku"].startswith("OLIST-WAGI-")

        # Verify Customer Ingestion without invented contact details
        cust = db.customers.find_one({"external_id": "c2001"})
        assert cust is not None
        assert cust["source"] == "olist_real"
        assert cust["city"] == "Sao Paulo"
        assert cust["state"] == "SP"
        assert cust.get("email") is None # Authentic: not invented

        # Verify Order Ingestion & Embedded Item Snapshots & Real Payments
        order = db.orders.find_one({"external_id": "ord3001"})
        assert order is not None
        assert order["source"] == "olist_real"
        assert order["status"] == "delivered"
        assert order["customer_id"] == cust["_id"]
        assert len(order["items"]) == 2
        assert order["subtotal"] == round(129.90 + 49.50, 2)
        assert order["shipping_address"]["city"] == "Sao Paulo"
        assert len(order.get("payments", [])) == 1
        assert order["payments"][0]["type"] == "credit_card"

        # Verify Review Ingestion & Rating Recalculation
        review = db.reviews.find_one({"external_id": "rev4001"})
        assert review is not None
        assert review["rating"] == 5
        assert "altissima qualidade" in review["review_text"]

        updated_prod = db.products.find_one({"external_id": "p1001"})
        assert updated_prod["rating_average"] == 5.0
        assert updated_prod["review_count"] >= 1

        # Verify Seller Ingestion
        seller = db.sellers.find_one({"external_id": "s501"})
        assert seller is not None
        assert seller["city"] == "Campinas"

        # Cleanup test records
        db.products.delete_many({"external_id": {"$in": ["p1001", "p1002"]}})
        db.customers.delete_many({"external_id": "c2001"})
        db.orders.delete_many({"external_id": "ord3001"})
        db.reviews.delete_many({"external_id": "rev4001"})
        db.sellers.delete_many({"external_id": "s501"})
