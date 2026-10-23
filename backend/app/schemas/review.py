from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class ReviewCreate(BaseModel):
    product_id: str = Field(..., description="Target product ObjectId string")
    customer_id: str = Field(..., description="Author customer ObjectId string")
    rating: int = Field(..., ge=1, le=5, description="Integer rating from 1 to 5")
    review_text: str = Field(..., min_length=3, max_length=1000, description="Review feedback")

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    review_text: Optional[str] = Field(None, min_length=3, max_length=1000)

class ReviewOut(BaseModel):
    id: str
    _id: Optional[str] = None
    product_id: str
    customer_id: str
    product_name: Optional[str] = None
    customer_name: Optional[str] = None
    rating: int
    review_text: str
    created_at: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True, extra="allow")
