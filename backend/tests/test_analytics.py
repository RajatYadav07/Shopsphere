import pytest

def test_dashboard_summary_endpoint(client):
    res = client.get("/api/v1/dashboard/summary")
    assert res.status_code == 200
    data = res.json()["data"]
    metrics = data["metrics"]
    assert metrics["total_revenue"] >= 0
    assert metrics["total_orders"] > 0
    assert metrics["total_customers"] > 0
    assert metrics["total_products"] > 0
    assert isinstance(data["monthly_trends"], list)
    assert isinstance(data["category_sales"], list)
    assert isinstance(data["top_products"], list)

def test_analytics_overview_and_csv_export(client):
    res = client.get("/api/v1/analytics/overview")
    assert res.status_code == 200
    data = res.json()["data"]
    assert "metrics" in data
    assert "repeat_customers" in data
    assert data["repeat_customers"]["total_customers"] > 0

    # Test CSV export
    csv_res = client.get("/api/v1/analytics/export-csv?report_type=category")
    assert csv_res.status_code == 200
    assert "text/csv" in csv_res.headers["content-type"]
    assert "Category,Total Revenue" in csv_res.text
