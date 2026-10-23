import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo.database import Database

from app.core.database import get_db
from app.repositories.customer_repository import CustomerRepository
from app.schemas.common import APIResponse, PaginatedResponse
from app.schemas.customer import CustomerCreate, CustomerDetailOut, CustomerOut, CustomerUpdate
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("", response_model=PaginatedResponse[CustomerOut])
def get_customers(
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Database = Depends(get_db)
):
    repo = CustomerRepository(db)
    skip = (page - 1) * page_size
    items, total = repo.find_all(skip=skip, limit=page_size, search=search)
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

@router.get("/{customer_id}", response_model=APIResponse[CustomerDetailOut])
def get_customer(customer_id: str, db: Database = Depends(get_db)):
    repo = CustomerRepository(db)
    cust = repo.find_by_id(customer_id)
    if not cust:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer '{customer_id}' not found")
    return APIResponse(data=cust)

@router.post("", response_model=APIResponse[CustomerOut], status_code=status.HTTP_201_CREATED)
def create_customer(customer_in: CustomerCreate, db: Database = Depends(get_db)):
    service = CustomerService(db)
    created, err = service.create_customer(customer_in)
    if err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)
    return APIResponse(message="Customer created successfully", data=created)

@router.put("/{customer_id}", response_model=APIResponse[CustomerOut])
def update_customer(customer_id: str, update_in: CustomerUpdate, db: Database = Depends(get_db)):
    service = CustomerService(db)
    updated, err = service.update_customer(customer_id, update_in)
    if err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)
    return APIResponse(message="Customer updated successfully", data=updated)

@router.delete("/{customer_id}", response_model=APIResponse[dict])
def delete_customer(customer_id: str, db: Database = Depends(get_db)):
    service = CustomerService(db)
    success, msg = service.delete_customer(customer_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
    return APIResponse(message=msg, data={"id": customer_id})
