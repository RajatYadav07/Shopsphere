from typing import Any, Dict, Optional, Tuple
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate

class CustomerService:
    def __init__(self, db: Database):
        self.db = db
        self.customer_repo = CustomerRepository(db)

    def create_customer(self, customer_in: CustomerCreate) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        existing = self.customer_repo.find_by_email(customer_in.email)
        if existing:
            return None, f"A customer with email '{customer_in.email}' already exists"

        try:
            created = self.customer_repo.create(customer_in.model_dump())
            return created, None
        except DuplicateKeyError:
            return None, f"Email '{customer_in.email}' is already registered (unique index violation)"
        except Exception as e:
            return None, str(e)

    def update_customer(self, customer_id: str, update_in: CustomerUpdate) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        existing = self.customer_repo.find_by_id(customer_id)
        if not existing:
            return None, "Customer not found"

        data = update_in.model_dump(exclude_unset=True)
        if "email" in data and data["email"] != existing.get("email"):
            email_check = self.customer_repo.find_by_email(data["email"])
            if email_check and email_check["id"] != customer_id:
                return None, f"Email '{data['email']}' is already in use by another customer"

        try:
            updated = self.customer_repo.update(customer_id, data)
            return updated, None
        except DuplicateKeyError:
            return None, "Unique email constraint violation"
        except Exception as e:
            return None, str(e)

    def delete_customer(self, customer_id: str) -> Tuple[bool, str]:
        return self.customer_repo.delete(customer_id)
