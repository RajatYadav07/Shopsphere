import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo.database import Database

from app.core.database import get_db
from app.repositories.order_repository import OrderRepository
from app.schemas.common import APIResponse, PaginatedResponse
from app.schemas.order import OrderCreate, OrderDetailOut, OrderOut, OrderStatusUpdate
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("", response_model=PaginatedResponse[OrderOut])
def get_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Database = Depends(get_db)
):
    repo = OrderRepository(db)
    skip = (page - 1) * page_size
    items, total = repo.find_all(
        skip=skip,
        limit=page_size,
        search=search,
        status=status,
        start_date=start_date,
        end_date=end_date
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

@router.get("/{order_id}", response_model=APIResponse[OrderDetailOut])
def get_order(order_id: str, db: Database = Depends(get_db)):
    repo = OrderRepository(db)
    order = repo.find_by_id(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order '{order_id}' not found")
    return APIResponse(data=order)

@router.post("", response_model=APIResponse[OrderOut], status_code=status.HTTP_201_CREATED)
def create_order(order_in: OrderCreate, db: Database = Depends(get_db)):
    service = OrderService(db)
    created, err = service.create_order(order_in)
    if err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)
    return APIResponse(message="Order created successfully and stock updated", data=created)

@router.patch("/{order_id}/status", response_model=APIResponse[dict])
def update_order_status(order_id: str, status_in: OrderStatusUpdate, db: Database = Depends(get_db)):
    service = OrderService(db)
    success, msg = service.update_order_status(order_id, status_in.status, status_in.reason)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
    return APIResponse(message=msg, data={"id": order_id, "status": status_in.status})
