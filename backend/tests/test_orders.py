import uuid
import pytest

def test_order_placement_stock_decrement_and_cancellation(client):
    # 1. Create a dedicated test product with known stock
    unique_suffix = uuid.uuid4().hex[:6].upper()
    prod_res = client.post("/api/v1/products", json={
        "name": f"Stock Test Product {unique_suffix}",
        "sku": f"STK-{unique_suffix}",
        "category": "Gaming Gear",
        "brand": "Razer",
        "description": "Stock testing item",
        "price": 100.0,
        "stock_quantity": 10,
        "tags": ["stock_test"]
    })
    assert prod_res.status_code == 201
    prod = prod_res.json()["data"]
    prod_id = prod["id"]

    # 2. Get a valid customer
    cust_res = client.get("/api/v1/customers?page=1&page_size=1")
    assert cust_res.status_code == 200
    cust = cust_res.json()["items"][0]
    cust_id = cust["id"]

    # 3. Test placing order with excessive quantity (insufficient stock)
    over_order = {
        "customer_id": cust_id,
        "items": [{"product_id": prod_id, "quantity": 99}],
        "shipping_address": {
            "street": "123 Test St",
            "city": "Austin",
            "state": "TX",
            "postal_code": "78701",
            "country": "USA"
        }
    }
    fail_res = client.post("/api/v1/orders", json=over_order)
    assert fail_res.status_code == 400
    assert "Insufficient stock" in fail_res.json()["detail"]

    # 4. Place valid order for 3 units
    valid_order = {
        "customer_id": cust_id,
        "items": [{"product_id": prod_id, "quantity": 3}],
        "shipping_address": {
            "street": "123 Test St",
            "city": "Austin",
            "state": "TX",
            "postal_code": "78701",
            "country": "USA"
        }
    }
    order_res = client.post("/api/v1/orders", json=valid_order)
    assert order_res.status_code == 201
    order_data = order_res.json()["data"]
    order_id = order_data["id"]
    assert order_data["subtotal"] == 300.0 # 3 * 100.0

    # 5. Verify stock was reduced from 10 to 7
    prod_check = client.get(f"/api/v1/products/{prod_id}")
    assert prod_check.json()["data"]["stock_quantity"] == 7

    # 6. Test invalid status transition: directly from pending to delivered
    inv_trans = client.patch(f"/api/v1/orders/{order_id}/status", json={"status": "delivered"})
    assert inv_trans.status_code == 400
    assert "Invalid transition" in inv_trans.json()["detail"]

    # 7. Cancel order and verify stock restoration
    cancel_res = client.patch(f"/api/v1/orders/{order_id}/status", json={
        "status": "cancelled",
        "reason": "Customer changed mind during test"
    })
    assert cancel_res.status_code == 200

    # 8. Verify stock restored back to 10
    restored_check = client.get(f"/api/v1/products/{prod_id}")
    assert restored_check.json()["data"]["stock_quantity"] == 10

    # Clean up test product
    client.delete(f"/api/v1/products/{prod_id}")
