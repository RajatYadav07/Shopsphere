import uuid
import pytest

def test_get_products_pagination(client):
    res = client.get("/api/v1/products?page=1&page_size=10")
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert len(data["items"]) <= 10
    assert data["total"] > 0

def test_product_crud_and_duplicate_sku(client):
    unique_suffix = uuid.uuid4().hex[:6].upper()
    test_sku = f"TEST-SKU-{unique_suffix}"

    new_prod = {
        "name": f"Test Mechanical Keyboard {unique_suffix}",
        "sku": test_sku,
        "category": "Computing & Accessories",
        "brand": "Keychron",
        "description": "Premium test keyboard with hot-swappable switches",
        "price": 129.99,
        "stock_quantity": 15,
        "tags": ["test", "keyboard"]
    }

    # 1. Create product
    create_res = client.post("/api/v1/products", json=new_prod)
    assert create_res.status_code == 201
    created_data = create_res.json()["data"]
    prod_id = created_data["id"]
    assert created_data["sku"] == test_sku

    # 2. Duplicate SKU rejection
    dup_res = client.post("/api/v1/products", json=new_prod)
    assert dup_res.status_code == 400
    assert "already exists" in dup_res.json()["detail"]

    # 3. Read product
    get_res = client.get(f"/api/v1/products/{prod_id}")
    assert get_res.status_code == 200
    assert get_res.json()["data"]["name"] == new_prod["name"]

    # 4. Update product
    update_res = client.put(f"/api/v1/products/{prod_id}", json={"price": 149.99})
    assert update_res.status_code == 200
    assert update_res.json()["data"]["price"] == 149.99

    # 5. Delete product
    del_res = client.delete(f"/api/v1/products/{prod_id}")
    assert del_res.status_code == 200

    # 6. Verify deleted
    get_after = client.get(f"/api/v1/products/{prod_id}")
    assert get_after.status_code == 404
