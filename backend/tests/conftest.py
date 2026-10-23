import os
import sys
import pytest
from datetime import datetime, timezone
from bson import ObjectId

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Enforce isolated test database
os.environ["DATABASE_NAME"] = "shopsphere_test"

from app.core.config import settings
settings.DATABASE_NAME = "shopsphere_test"

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import db_manager, utc_now
from app.core.indexes import create_all_indexes
from app.core.validators import apply_collection_validators

@pytest.fixture(scope="session", autouse=True)
def setup_isolated_test_database():
    """Initializes and seeds an isolated test database (shopsphere_test)."""
    # Connect to MongoDB
    db_manager.connect()
    db = db_manager.get_database()
    assert db.name == "shopsphere_test", f"Safety check failed: connected to '{db.name}', expected 'shopsphere_test'!"

    # Clean previous test database records
    for col in ["products", "customers", "orders", "reviews", "inventory_movements", "shopsphere_demo"]:
        db[col].delete_many({})

    # Apply schema validators and indexes
    apply_collection_validators(db)
    create_all_indexes(db)

    # Seed baseline isolated fixtures for tests
    cust1_id = ObjectId()
    cust2_id = ObjectId()
    prod1_id = ObjectId()
    prod2_id = ObjectId()
    now = datetime(2026, 3, 1, 12, 0, 0, tzinfo=timezone.utc)

    db.customers.insert_many([
        {
            "_id": cust1_id,
            "name": "Test Customer Alpha",
            "email": "test.alpha@example.com",
            "phone": "+1-555-0101",
            "address": "100 Test Blvd",
            "city": "Austin",
            "source": "test",
            "created_at": now
        },
        {
            "_id": cust2_id,
            "name": "Test Customer Beta",
            "email": "test.beta@example.com",
            "phone": "+1-555-0102",
            "address": "200 Test Blvd",
            "city": "Dallas",
            "source": "test",
            "created_at": now
        }
    ])

    db.products.insert_many([
        {
            "_id": prod1_id,
            "name": "Pro Wireless Mechanical Keyboard",
            "sku": "TEST-KB-001",
            "category": "Computing & Accessories",
            "brand": "Keychron",
            "description": "High performance mechanical test keyboard",
            "price": 99.99,
            "stock_quantity": 25,
            "inventory_tracked": True,
            "tags": ["keyboard", "test"],
            "rating_average": 5.0,
            "review_count": 1,
            "source": "test",
            "created_at": now,
            "updated_at": now
        },
        {
            "_id": prod2_id,
            "name": "Precision Ergonomic Mouse",
            "sku": "TEST-MS-002",
            "category": "Computing & Accessories",
            "brand": "Logitech",
            "description": "High precision wireless mouse",
            "price": 49.99,
            "stock_quantity": 30,
            "inventory_tracked": True,
            "tags": ["mouse", "test"],
            "rating_average": 4.5,
            "review_count": 1,
            "source": "test",
            "created_at": now,
            "updated_at": now
        }
    ])

    db.orders.insert_many([
        {
            "_id": ObjectId(),
            "customer_id": cust1_id,
            "items": [
                {
                    "product_id": str(prod1_id),
                    "name": "Pro Wireless Mechanical Keyboard",
                    "sku": "TEST-KB-001",
                    "category": "Computing & Accessories",
                    "unit_price": 99.99,
                    "quantity": 1,
                    "line_total": 99.99
                }
            ],
            "shipping_address": {
                "street": "100 Test Blvd",
                "city": "Austin",
                "state": "TX",
                "postal_code": "78701",
                "country": "USA"
            },
            "subtotal": 99.99,
            "status": "delivered",
            "source": "test",
            "created_at": now,
            "updated_at": now
        },
        {
            "_id": ObjectId(),
            "customer_id": cust1_id, # Repeat order for repeat customer metrics
            "items": [
                {
                    "product_id": str(prod2_id),
                    "name": "Precision Ergonomic Mouse",
                    "sku": "TEST-MS-002",
                    "category": "Computing & Accessories",
                    "unit_price": 49.99,
                    "quantity": 1,
                    "line_total": 49.99
                }
            ],
            "shipping_address": {
                "street": "100 Test Blvd",
                "city": "Austin",
                "state": "TX",
                "postal_code": "78701",
                "country": "USA"
            },
            "subtotal": 49.99,
            "status": "delivered",
            "source": "test",
            "created_at": now,
            "updated_at": now
        }
    ])

    db.reviews.insert_one({
        "_id": ObjectId(),
        "product_id": prod1_id,
        "customer_id": cust1_id,
        "rating": 5,
        "review_text": "Superb quality test product",
        "source": "test",
        "created_at": now
    })

    db.shopsphere_demo.insert_many([
        {"item_name": "Demo RGB Mouse", "category": "Peripherals", "price": 49.99, "stock": 40, "created_at": now},
        {"item_name": "Demo USB Hub", "category": "Accessories", "price": 29.99, "stock": 65, "created_at": now}
    ])

    yield

    # Clean up after test session finishes
    for col in ["products", "customers", "orders", "reviews", "inventory_movements", "shopsphere_demo"]:
        db[col].delete_many({"source": "test"})

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="session")
def db():
    return db_manager.get_database()
