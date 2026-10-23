from typing import Any, Dict, Optional, Tuple
from pymongo.database import Database

from app.repositories.inventory_repository import InventoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.inventory import StockAdjustmentCreate

class InventoryService:
    def __init__(self, db: Database):
        self.db = db
        self.inv_repo = InventoryRepository(db)
        self.product_repo = ProductRepository(db)

    def adjust_stock(self, adj_in: StockAdjustmentCreate) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        product = self.product_repo.find_by_id(adj_in.product_id)
        if not product:
            return None, "Product not found"

        current_stock = product.get("stock_quantity", 0)
        if adj_in.change_quantity < 0 and abs(adj_in.change_quantity) > current_stock:
            return None, f"Cannot reduce stock by {abs(adj_in.change_quantity)}. Current available stock is only {current_stock}."

        updated = self.product_repo.adjust_stock(adj_in.product_id, adj_in.change_quantity)
        if not updated:
            return None, "Failed to update stock quantity"

        movement = self.inv_repo.record_movement(
            product_id=adj_in.product_id,
            change_quantity=adj_in.change_quantity,
            reason=adj_in.reason,
            related_order_id=adj_in.related_order_id
        )

        return movement, None

    def get_inventory_summary(self) -> Dict[str, Any]:
        low_stock_docs, _ = self.product_repo.find_all(stock_status="low_stock", limit=50)
        out_of_stock_docs, _ = self.product_repo.find_all(stock_status="out_of_stock", limit=50)
        movements, total_movements = self.inv_repo.find_all(limit=10)

        # Aggregate total units in stock for tracked items
        pipeline = [
            {"$match": {"inventory_tracked": True}},
            {"$group": {"_id": None, "total_units": {"$sum": "$stock_quantity"}}}
        ]
        res = list(self.db["products"].aggregate(pipeline))
        total_units = res[0]["total_units"] if res else 0

        total_catalog = self.db["products"].count_documents({})
        historical_catalog_count = self.db["products"].count_documents({"inventory_tracked": {"$ne": True}})
        tracked_inventory_count = self.db["products"].count_documents({"inventory_tracked": True})

        return {
            "total_units_in_stock": total_units,
            "total_catalog_count": total_catalog,
            "historical_catalog_count": historical_catalog_count,
            "tracked_inventory_count": tracked_inventory_count,
            "low_stock_count": len(low_stock_docs),
            "out_of_stock_count": len(out_of_stock_docs),
            "total_movement_records": total_movements,
            "low_stock_products": low_stock_docs,
            "out_of_stock_products": out_of_stock_docs,
            "recent_movements": movements,
            "olist_notice": "Genuine warehouse inventory levels are not present in the Olist public dataset. Inventory movements and real-time stock tracking apply to operational inventory."
        }
