from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class DashboardMetrics(BaseModel):
    total_revenue: float
    total_orders: int
    total_customers: int
    total_products: int
    pending_orders: int
    low_stock_products_count: int
    average_order_value: float

class MonthlyTrendPoint(BaseModel):
    month: str # e.g. "2026-05"
    revenue: float
    orders_count: int

class CategorySalesPoint(BaseModel):
    category: str
    total_revenue: float
    units_sold: int
    order_count: int

class TopSellingProduct(BaseModel):
    product_id: str
    name: str
    sku: str
    category: str
    units_sold: int
    total_revenue: float

class StatusDistributionPoint(BaseModel):
    status: str
    count: int
    percentage: float

class RatingDistributionPoint(BaseModel):
    rating: int
    count: int

class RepeatCustomerMetrics(BaseModel):
    total_customers: int
    repeat_customers: int
    repeat_customer_rate: float
    single_order_customers: int
    average_orders_per_customer: float

class AnalyticsReportOut(BaseModel):
    metrics: DashboardMetrics
    monthly_trends: List[MonthlyTrendPoint]
    category_sales: List[CategorySalesPoint]
    top_products: List[TopSellingProduct]
    status_distribution: List[StatusDistributionPoint]
    repeat_customers: RepeatCustomerMetrics
    rating_distribution: List[RatingDistributionPoint]
