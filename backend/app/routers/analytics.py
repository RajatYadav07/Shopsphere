import csv
import io
from typing import Optional
from fastapi import APIRouter, Depends, Query, Response
from pymongo.database import Database

from app.core.database import get_db
from app.repositories.analytics_repository import AnalyticsRepository
from app.schemas.common import APIResponse

router = APIRouter(prefix="/analytics", tags=["Analytics & Reports"])

@router.get("/overview", response_model=APIResponse[dict])
def get_analytics_overview(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Database = Depends(get_db)
):
    repo = AnalyticsRepository(db)
    metrics = repo.get_dashboard_metrics(start_date=start_date, end_date=end_date)
    monthly_trends = repo.get_monthly_revenue_trends()
    category_sales = repo.get_category_sales()
    top_products = repo.get_top_selling_products(limit=10)
    status_dist = repo.get_order_status_distribution()
    rating_dist = repo.get_rating_distribution()
    repeat_customers = repo.get_repeat_customer_metrics()

    return APIResponse(data={
        "metrics": metrics,
        "monthly_trends": monthly_trends,
        "category_sales": category_sales,
        "top_products": top_products,
        "status_distribution": status_dist,
        "rating_distribution": rating_dist,
        "repeat_customers": repeat_customers
    })

@router.get("/export-csv")
def export_csv_report(
    report_type: str = Query("category", pattern="^(category|monthly|top_products)$"),
    db: Database = Depends(get_db)
):
    repo = AnalyticsRepository(db)
    output = io.StringIO()
    writer = csv.writer(output)

    if report_type == "category":
        writer.writerow(["Category", "Total Revenue ($)", "Units Sold", "Order Count"])
        for row in repo.get_category_sales():
            writer.writerow([row.get("category"), row.get("total_revenue"), row.get("units_sold"), row.get("order_count")])
        filename = "shopsphere_category_sales_report.csv"

    elif report_type == "monthly":
        writer.writerow(["Month", "Revenue ($)", "Order Count"])
        for row in repo.get_monthly_revenue_trends():
            writer.writerow([row.get("month"), row.get("revenue"), row.get("orders_count")])
        filename = "shopsphere_monthly_revenue_report.csv"

    else:
        writer.writerow(["Product ID", "Product Name", "SKU", "Category", "Units Sold", "Total Revenue ($)"])
        for row in repo.get_top_selling_products(limit=50):
            writer.writerow([row.get("product_id"), row.get("name"), row.get("sku"), row.get("category"), row.get("units_sold"), row.get("total_revenue")])
        filename = "shopsphere_top_products_report.csv"

    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
