import pytest

def test_crud_demo_endpoints(client):
    # Test insertOne
    res1 = client.post("/api/v1/concepts/crud", json={"operation": "insertOne", "payload": {"item_name": "Test Wireless Mouse", "price": 45.0, "stock": 20}})
    assert res1.status_code == 200
    assert res1.json()["data"]["operation"] == "insertOne"
    assert res1.json()["data"]["affected_count"] == 1

    # Test find
    res2 = client.post("/api/v1/concepts/crud", json={"operation": "find", "payload": {"limit": 5}})
    assert res2.status_code == 200
    assert isinstance(res2.json()["data"]["result"], list)

    # Test updateOne
    res3 = client.post("/api/v1/concepts/crud", json={"operation": "updateOne"})
    assert res3.status_code == 200
    assert res3.json()["data"]["operation"] == "updateOne"

def test_aggregation_playground_queries(client):
    # Test all 8 aggregation presets
    for q_id in range(1, 9):
        res = client.post("/api/v1/concepts/aggregation", json={"query_id": str(q_id)})
        assert res.status_code == 200, f"Query {q_id} failed"
        data = res.json()["data"]
        assert data["query_id"] == str(q_id)
        assert len(data["stages_used"]) > 0
        assert "pipeline_code" in data
        assert isinstance(data["result"], list)

def test_explain_query_plan(client):
    # Test index scan explain
    res = client.post("/api/v1/concepts/explain", json={"scenario": "find_by_sku", "force_collscan": False})
    assert res.status_code == 200
    data = res.json()["data"]
    assert "nReturned" in data
    assert "totalKeysExamined" in data
    assert "stage" in data

def test_schema_validation_demo(client):
    # 1. Valid insert
    valid_res = client.post("/api/v1/concepts/validation", json={
        "test_type": "valid",
        "item_name": "Valid Test Gadget",
        "price": 49.99,
        "stock": 10
    })
    assert valid_res.status_code == 200
    assert valid_res.json()["data"]["accepted"] is True

    # 2. Invalid insert (rejected by MongoDB $jsonSchema)
    invalid_res = client.post("/api/v1/concepts/validation", json={
        "test_type": "invalid",
        "item_name": "Invalid Price Gadget",
        "price": -50.0, # Negative price triggers violation
        "stock": 5
    })
    assert invalid_res.status_code == 200
    inv_data = invalid_res.json()["data"]
    assert inv_data["accepted"] is False
    assert "REJECTED by MongoDB $jsonSchema Validator" in inv_data["status_message"]
