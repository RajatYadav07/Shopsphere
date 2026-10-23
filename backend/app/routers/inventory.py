import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo.database import Database

from app.core.database import get_db
from app.repositories.inventory_repository import InventoryRepository
from app.schemas.common import APIResponse, PaginatedResponse
from app.schemas.inventory import InventoryMovementOut, StockAdjustmentCreate
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/summary", response_model=APIResponse[dict])
def get_inventory_summary(db: Database = Depends(get_db)):
    service = InventoryService(db)
    summary = service.get_inventory_summary()
    return APIResponse(data=summary)

@router.get("/movements", response_model=PaginatedResponse[InventoryMovementOut])
def get_inventory_movements(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    product_id: Optional[str] = Query(None),
    db: Database = Depends(get_db)
):
    repo = InventoryRepository(db)
    skip = (page - 1) * page_size
    items, total = repo.find_all(skip=skip, limit=page_size, product_id=product_id)
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

@router.post("/adjust", response_model=APIResponse[InventoryMovementOut], status_code=status.HTTP_201_CREATED)
def adjust_inventory_stock(adj_in: StockAdjustmentCreate, db: Database = Depends(get_db)):
    service = InventoryService(db)
    movement, err = service.adjust_stock(adj_in)
    if err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)
    return APIResponse(message="Inventory adjusted successfully and movement recorded", data=movement)
