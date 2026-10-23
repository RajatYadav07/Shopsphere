from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class StockAdjustmentType(str, Enum):
    STOCK_IN = "stock_in"
    STOCK_OUT = "stock_out"
    ADJUSTMENT = "adjustment"

class StockAdjustmentCreate(BaseModel):
    product_id: str
    change_quantity: int = Field(..., description="Positive for addition, negative for reduction")
    reason: str = Field(..., min_length=3, max_length=200, description="Audit reason for stock change")
    related_order_id: Optional[str] = None

class InventoryMovementOut(BaseModel):
    id: str
    _id: Optional[str] = None
    product_id: str
    product_name: Optional[str] = None
    sku: Optional[str] = None
    change_quantity: int
    reason: str
    related_order_id: Optional[str] = None
    created_at: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True, extra="allow")

class LowStockProduct(BaseModel):
    id: str
    _id: Optional[str] = None
    name: str
    sku: str
    category: str
    price: float
    stock_quantity: int

    model_config = ConfigDict(populate_by_name=True, extra="allow")
