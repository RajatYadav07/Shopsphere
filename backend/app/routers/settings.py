from fastapi import APIRouter, Depends
from pymongo.database import Database

from app.core.database import db_manager, get_db
from app.core.indexes import create_all_indexes, get_indexes_summary
from app.schemas.common import APIResponse

router = APIRouter(prefix="/settings", tags=["Settings & System"])

@router.get("/health", response_model=APIResponse[dict])
def check_system_health():
    status_info = db_manager.check_connection()
    return APIResponse(data=status_info)

@router.post("/recreate-indexes", response_model=APIResponse[dict])
def recreate_indexes(db: Database = Depends(get_db)):
    created = create_all_indexes(db)
    return APIResponse(message="Indexes verified and updated", data=created)

@router.get("/stats", response_model=APIResponse[dict])
def get_database_stats(db: Database = Depends(get_db)):
    collections = ["products", "customers", "orders", "reviews", "inventory_movements", "shopsphere_demo"]
    counts = {}
    for col in collections:
        try:
            counts[col] = db[col].count_documents({})
        except Exception:
            counts[col] = 0

    conn = db_manager.check_connection()
    return APIResponse(data={
        "database_name": db.name,
        "collections_count": len(db.list_collection_names()),
        "collection_document_counts": counts,
        "server_version": conn.get("server_version"),
        "topology": conn.get("topology"),
        "transactions_supported": conn.get("transactions_supported")
    })
