import uuid
import pytest

def test_customer_crud_and_email_uniqueness(client):
    suffix = uuid.uuid4().hex[:6]
    test_email = f"test.user.{suffix}@example.com"

    customer_data = {
        "name": f"Test Customer {suffix}",
        "email": test_email,
        "phone": "+1-555-9999",
        "address": "99 Innovation Way",
        "city": "Palo Alto"
    }

    # 1. Create customer
    res = client.post("/api/v1/customers", json=customer_data)
    assert res.status_code == 201
    created = res.json()["data"]
    cid = created["id"]
    assert created["email"] == test_email

    # 2. Duplicate email rejection
    dup_res = client.post("/api/v1/customers", json=customer_data)
    assert dup_res.status_code == 400
    assert "already exists" in dup_res.json()["detail"]

    # 3. Read customer details
    get_res = client.get(f"/api/v1/customers/{cid}")
    assert get_res.status_code == 200
    assert get_res.json()["data"]["name"] == customer_data["name"]

    # 4. Update customer
    up_res = client.put(f"/api/v1/customers/{cid}", json={"city": "San Jose"})
    assert up_res.status_code == 200
    assert up_res.json()["data"]["city"] == "San Jose"

    # 5. Delete customer
    del_res = client.delete(f"/api/v1/customers/{cid}")
    assert del_res.status_code == 200
