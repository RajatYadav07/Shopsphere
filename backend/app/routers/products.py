import math
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo.database import Database

from app.core.database import get_db
from app.repositories.product_repository import ProductRepository
from app.schemas.common import APIResponse, PaginatedResponse
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("", response_model=PaginatedResponse[ProductOut])
def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    stock_status: Optional[str] = Query(None, pattern="^(in_stock|low_stock|out_of_stock)$"),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    db: Database = Depends(get_db)
):
    repo = ProductRepository(db)
    skip = (page - 1) * page_size
    items, total = repo.find_all(
        skip=skip,
        limit=page_size,
        search=search,
        category=category,
        brand=brand,
        min_price=min_price,
        max_price=max_price,
        stock_status=stock_status,
        sort_by=sort_by,
        sort_order=sort_order
    )
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

@router.get("/meta/categories", response_model=List[str])
def get_categories(db: Database = Depends(get_db)):
    repo = ProductRepository(db)
    return repo.get_categories()

@router.get("/meta/brands", response_model=List[str])
def get_brands(db: Database = Depends(get_db)):
    repo = ProductRepository(db)
    return repo.get_brands()

@router.get("/{product_id}", response_model=APIResponse[ProductOut])
def get_product(product_id: str, db: Database = Depends(get_db)):
    repo = ProductRepository(db)
    prod = repo.find_by_id(product_id)
    if not prod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID '{product_id}' not found")
    return APIResponse(data=prod)

@router.post("", response_model=APIResponse[ProductOut], status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductCreate, db: Database = Depends(get_db)):
    service = ProductService(db)
    created, err = service.create_product(product_in)
    if err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)
    return APIResponse(message="Product created successfully", data=created)

@router.put("/{product_id}", response_model=APIResponse[ProductOut])
def update_product(product_id: str, update_in: ProductUpdate, db: Database = Depends(get_db)):
    service = ProductService(db)
    updated, err = service.update_product(product_id, update_in)
    if err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)
    return APIResponse(message="Product updated successfully", data=updated)

@router.delete("/{product_id}", response_model=APIResponse[dict])
def delete_product(product_id: str, db: Database = Depends(get_db)):
    service = ProductService(db)
    success, msg = service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
    return APIResponse(message=msg, data={"id": product_id})
