from typing import Any, Dict, Optional, Tuple
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self, db: Database):
        self.db = db
        self.product_repo = ProductRepository(db)

    def create_product(self, product_in: ProductCreate) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        # Check duplicate SKU
        existing = self.product_repo.find_by_sku(product_in.sku)
        if existing:
            return None, f"A product with SKU '{product_in.sku}' already exists"

        try:
            created = self.product_repo.create(product_in.model_dump())
            return created, None
        except DuplicateKeyError:
            return None, f"Duplicate SKU '{product_in.sku}' rejected by database index"
        except Exception as e:
            return None, str(e)

    def update_product(self, product_id: str, update_in: ProductUpdate) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        existing = self.product_repo.find_by_id(product_id)
        if not existing:
            return None, "Product not found"

        try:
            updated = self.product_repo.update(product_id, update_in.model_dump(exclude_unset=True))
            return updated, None
        except DuplicateKeyError:
            return None, "Unique constraint violation: duplicate SKU"
        except Exception as e:
            return None, str(e)

    def delete_product(self, product_id: str) -> Tuple[bool, str]:
        existing = self.product_repo.find_by_id(product_id)
        if not existing:
            return False, "Product not found"

        # Check if product is in any active order
        order_with_prod = self.db["orders"].find_one({"items.product_id": product_id})
        if order_with_prod:
            return False, "Cannot delete product referenced in existing order history. Consider setting stock to 0."

        deleted = self.product_repo.delete(product_id)
        return deleted, "Product deleted successfully" if deleted else "Failed to delete product"
