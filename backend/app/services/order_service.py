import logging
from typing import Any, Dict, List, Optional, Tuple
from bson import ObjectId
from pymongo.database import Database
from pymongo.errors import PyMongoError

from app.core.database import db_manager, utc_now
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.inventory_repository import InventoryRepository
from app.schemas.order import OrderCreate, OrderStatus, VALID_TRANSITIONS

logger = logging.getLogger("shopsphere.order_service")

class OrderService:
    def __init__(self, db: Database):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.product_repo = ProductRepository(db)
        self.customer_repo = CustomerRepository(db)
        self.inventory_repo = InventoryRepository(db)

    def create_order(self, order_in: OrderCreate) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Create order with:
        - Customer validation
        - Stock verification and reduction
        - Item snapshot generation
        - Inventory movement logging
        - Automatic fallback to atomic two-phase updates on standalone MongoDB
        """
        # 1. Validate Customer
        try:
            cust_oid = ObjectId(order_in.customer_id)
        except Exception:
            return None, "Invalid customer ID format"

        customer = self.db["customers"].find_one({"_id": cust_oid})
        if not customer:
            return None, f"Customer with ID {order_in.customer_id} does not exist"

        # 2. Check stock and prepare snapshots
        snapshots = []
        subtotal = 0.0
        allocated_items: List[Tuple[str, int]] = []

        for item in order_in.items:
            product = self.product_repo.find_by_id(item.product_id)
            if not product:
                return None, f"Product {item.product_id} not found"

            is_tracked = product.get("inventory_tracked", False)
            current_stock = product.get("stock_quantity", 0)
            if is_tracked and current_stock < item.quantity:
                return None, f"Insufficient stock for '{product.get('name')}'. Available: {current_stock}, Requested: {item.quantity}"

            line_total = round(product["price"] * item.quantity, 2)
            subtotal += line_total
            snapshots.append({
                "product_id": str(product["id"]),
                "name": product["name"],
                "sku": product["sku"],
                "category": product.get("category", "General"),
                "unit_price": float(product["price"]),
                "quantity": int(item.quantity),
                "line_total": line_total
            })

        subtotal = round(subtotal, 2)

        # 3. Determine if transactions are supported
        conn_info = db_manager.check_connection()
        supports_tx = conn_info.get("transactions_supported", False)

        order_doc = {
            "customer_id": cust_oid,
            "items": snapshots,
            "shipping_address": order_in.shipping_address.model_dump(),
            "notes": order_in.notes or "Demo Storefront Checkout",
            "subtotal": subtotal,
            "status": OrderStatus.PENDING.value,
            "source": "demo",
            "is_historical": False,
            "created_at": utc_now(),
            "updated_at": utc_now()
        }

        tracked_items = [
            item for item in order_in.items
            if (self.product_repo.find_by_id(item.product_id) or {}).get("inventory_tracked", False)
        ]

        if supports_tx and db_manager.client:
            # Multi-document ACID Transaction (ReplicaSet)
            try:
                with db_manager.client.start_session() as session:
                    with session.start_transaction():
                        created_order = self.order_repo.create(order_doc, session=session)
                        for item in tracked_items:
                            reduced = self.product_repo.adjust_stock(item.product_id, -item.quantity, session=session)
                            if not reduced:
                                raise ValueError(f"Failed to reduce stock for product {item.product_id}")
                            self.inventory_repo.record_movement(
                                product_id=item.product_id,
                                change_quantity=-item.quantity,
                                reason=f"Demo Order #{created_order['id']}",
                                related_order_id=created_order["id"],
                                session=session
                            )
                return created_order, None
            except Exception as e:
                logger.error(f"Transaction failed: {e}")
                return None, f"Order placement failed: {str(e)}"
        else:
            # Standalone MongoDB Safe Fallback with Compensation
            for item in tracked_items:
                success = self.product_repo.adjust_stock(item.product_id, -item.quantity)
                if not success:
                    for roll_pid, roll_qty in allocated_items:
                        self.product_repo.adjust_stock(roll_pid, roll_qty)
                    return None, f"Concurrent order conflict: insufficient stock for product {item.product_id}"
                allocated_items.append((item.product_id, item.quantity))

            try:
                created_order = self.order_repo.create(order_doc)
                for item in order_in.items:
                    self.inventory_repo.record_movement(
                        product_id=item.product_id,
                        change_quantity=-item.quantity,
                        reason=f"Demo Order #{created_order['id']}",
                        related_order_id=created_order["id"]
                    )
                return created_order, None
            except Exception as e:
                for roll_pid, roll_qty in allocated_items:
                    self.product_repo.adjust_stock(roll_pid, roll_qty)
                return None, f"Failed to persist order document: {str(e)}"

    def update_order_status(self, order_id: str, new_status: OrderStatus, reason: Optional[str] = None) -> Tuple[bool, str]:
        order = self.order_repo.find_by_id(order_id)
        if not order:
            return False, "Order not found"

        if order.get("source") == "olist_real" or order.get("is_historical"):
            return False, "Cannot modify historical Olist transaction. Historical dataset records are immutable."

        current_status = OrderStatus(order["status"])
        allowed_next = VALID_TRANSITIONS.get(current_status, [])

        if new_status not in allowed_next:
            return False, f"Invalid transition: Cannot move order from '{current_status.value}' to '{new_status.value}'. Allowed: {[s.value for s in allowed_next]}"

        # If transitioning to CANCELLED from PENDING or CONFIRMED, restore stock
        if new_status == OrderStatus.CANCELLED and current_status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
            for item in order.get("items", []):
                pid = item.get("product_id")
                qty = item.get("quantity", 0)
                if pid and qty > 0:
                    prod = self.product_repo.find_by_id(pid)
                    if prod and prod.get("inventory_tracked", False):
                        self.product_repo.adjust_stock(pid, qty)
                    self.inventory_repo.record_movement(
                        product_id=pid,
                        change_quantity=qty,
                        reason=f"Restored stock from cancelled demo order #{order_id}. {reason or ''}".strip(),
                        related_order_id=order_id
                    )

        updated = self.order_repo.update_status(order_id, new_status.value)
        return updated, f"Order status updated to {new_status.value}"
