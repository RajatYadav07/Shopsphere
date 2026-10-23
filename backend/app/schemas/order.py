from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

VALID_TRANSITIONS = {
    OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
    OrderStatus.CONFIRMED: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
    OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
    OrderStatus.DELIVERED: [], # Terminal state
    OrderStatus.CANCELLED: [], # Terminal state
}

class ShippingAddress(BaseModel):
    street: Optional[str] = ""
    city: str = Field(..., min_length=2)
    state: Optional[str] = ""
    postal_code: Optional[str] = ""
    country: str = Field(default="Brazil")

class OrderItemInput(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0, description="Quantity ordered")

class OrderItemSnapshot(BaseModel):
    product_id: str
    name: str
    sku: str
    unit_price: float
    quantity: int
    line_total: float
    category: Optional[str] = None
    freight_value: Optional[float] = 0.0
    seller_id: Optional[str] = None

class OrderCreate(BaseModel):
    customer_id: str
    items: List[OrderItemInput] = Field(..., min_length=1)
    shipping_address: ShippingAddress
    notes: Optional[str] = ""

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
    reason: Optional[str] = ""

class OrderOut(BaseModel):
    id: str
    _id: Optional[str] = None
    customer_id: str
    items: List[OrderItemSnapshot]
    shipping_address: ShippingAddress
    subtotal: float
    status: OrderStatus
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    source: Optional[str] = None
    external_id: Optional[str] = None
    is_historical: Optional[bool] = None
    freight_total: Optional[float] = 0.0
    total_amount: Optional[float] = None
    payments: Optional[List[Dict[str, Any]]] = None

    model_config = ConfigDict(populate_by_name=True, extra="allow")

class OrderDetailOut(OrderOut):
    customer: Optional[Dict[str, Any]] = None
