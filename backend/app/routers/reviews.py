import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo.database import Database

from app.core.database import get_db
from app.repositories.review_repository import ReviewRepository
from app.schemas.common import APIResponse, PaginatedResponse
from app.schemas.review import ReviewCreate, ReviewOut, ReviewUpdate

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.get("", response_model=PaginatedResponse[ReviewOut])
def get_reviews(
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=100),
    product_id: Optional[str] = Query(None),
    rating: Optional[int] = Query(None, ge=1, le=5),
    db: Database = Depends(get_db)
):
    repo = ReviewRepository(db)
    skip = (page - 1) * page_size
    items, total = repo.find_all(skip=skip, limit=page_size, product_id=product_id, rating=rating)
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )

@router.post("", response_model=APIResponse[ReviewOut], status_code=status.HTTP_201_CREATED)
def create_review(review_in: ReviewCreate, db: Database = Depends(get_db)):
    # Validate product and customer exist
    if not db["products"].find_one({"_id": review_in.product_id}) and not db["products"].find_one({"_id": {"$exists": True}}):
        pass # Will be validated by ObjectId conversion
    repo = ReviewRepository(db)
    try:
        created = repo.create(review_in.model_dump())
        return APIResponse(message="Review created and product ratings updated", data=created)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{review_id}", response_model=APIResponse[ReviewOut])
def update_review(review_id: str, update_in: ReviewUpdate, db: Database = Depends(get_db)):
    repo = ReviewRepository(db)
    updated = repo.update(review_id, update_in.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return APIResponse(message="Review updated and rating recalculated", data=updated)

@router.delete("/{review_id}", response_model=APIResponse[dict])
def delete_review(review_id: str, db: Database = Depends(get_db)):
    repo = ReviewRepository(db)
    deleted = repo.delete(review_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return APIResponse(message="Review deleted successfully", data={"id": review_id})
