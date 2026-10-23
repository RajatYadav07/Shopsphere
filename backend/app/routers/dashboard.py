from typing import Optional
from fastapi import APIRouter, Depends, Query
from pymongo.database import Database

from app.core.database import get_db
from app.repositories.analytics_repository import AnalyticsRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.common import APIResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=APIResponse[dict])
def get_dashboard_summary(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Database = Depends(get_db)
):
    analytics = AnalyticsRepository(db)
    order_repo = OrderRepository(db)
    product_repo = ProductRepository(db)

    metrics = analytics.get_dashboard_metrics(start_date=start_date, end_date=end_date)
    monthly_trends = analytics.get_monthly_revenue_trends()
    category_sales = analytics.get_category_sales()
    top_products = analytics.get_top_selling_products(limit=5)
    recent_orders, _ = order_repo.find_all(skip=0, limit=6)
    low_stock_products, _ = product_repo.find_all(stock_status="low_stock", limit=6)

    return APIResponse(data={
        "metrics": metrics,
        "monthly_trends": monthly_trends,
        "category_sales": category_sales,
        "top_products": top_products,
        "recent_orders": recent_orders,
        "low_stock_alerts": low_stock_products
    })
