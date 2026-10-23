from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150, description="Product title")
    sku: str = Field(..., min_length=3, max_length=50, description="Unique Stock Keeping Unit")
    category: str = Field(..., min_length=2, max_length=80, description="Product category")
    brand: str = Field(..., min_length=2, max_length=80, description="Product brand name")
    description: Optional[str] = Field(default="", description="Product full description")
    price: float = Field(..., gt=0, description="Product unit price in USD, must be greater than 0")
    stock_quantity: int = Field(default=0, ge=0, description="Available stock quantity, non-negative")
    inventory_tracked: bool = Field(default=True, description="Whether warehouse inventory is actively tracked")
    tags: List[str] = Field(default_factory=list, description="Categorization tags")
    image_url: Optional[str] = Field(default=None, description="Optional product image URL")
    source: Optional[str] = Field(default="direct", description="Data source")
    external_id: Optional[str] = Field(default=None, description="External Olist product ID")

    @field_validator("sku")
    @classmethod
    def clean_sku(cls, v: str) -> str:
        return v.strip().upper()

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=150)
    category: Optional[str] = Field(None, min_length=2, max_length=80)
    brand: Optional[str] = Field(None, min_length=2, max_length=80)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None

class ProductOut(ProductBase):
    id: str
    _id: Optional[str] = None
    rating_average: float = 0.0
    review_count: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True, extra="allow")
