from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Customer full name")
    email: Optional[str] = Field(default=None, description="Customer email address (optional for anonymized Olist data)")
    phone: Optional[str] = Field(default=None, max_length=30, description="Contact phone number")
    address: Optional[str] = Field(default=None, max_length=200, description="Street address")
    city: Optional[str] = Field(default=None, max_length=100, description="City")
    state: Optional[str] = Field(default=None, max_length=20, description="State")
    zip_code_prefix: Optional[str] = Field(default=None, max_length=20, description="ZIP code prefix")
    source: Optional[str] = Field(default="direct", description="Data source")
    external_id: Optional[str] = Field(default=None, description="External Olist customer ID")
    external_unique_id: Optional[str] = Field(default=None, description="External Olist customer unique ID")

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None

class CustomerOut(CustomerBase):
    id: str
    _id: Optional[str] = None
    created_at: Optional[str] = None
    total_spent: float = 0.0
    total_orders: int = 0
    average_order_value: float = 0.0

    model_config = ConfigDict(populate_by_name=True, extra="allow")

class CustomerDetailOut(CustomerOut):
    order_history: List[Dict[str, Any]] = Field(default_factory=list)
