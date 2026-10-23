import logging
from pymongo.database import Database

logger = logging.getLogger("shopsphere.validators")

# MongoDB JSON Schema Validators
PRODUCT_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "sku", "category", "price", "stock_quantity"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "Product name is required and must be a string"
            },
            "sku": {
                "bsonType": "string",
                "description": "Unique SKU identifier string"
            },
            "category": {
                "bsonType": "string",
                "description": "Product category string"
            },
            "price": {
                "bsonType": ["double", "int", "decimal"],
                "minimum": 0.01,
                "description": "Price must be a positive number (> 0)"
            },
            "stock_quantity": {
                "bsonType": "int",
                "minimum": 0,
                "description": "Stock quantity must be a non-negative integer (>= 0)"
            },
            "rating_average": {
                "bsonType": ["double", "int", "decimal"],
                "minimum": 0,
                "maximum": 5,
                "description": "Average rating between 0 and 5"
            }
        }
    }
}

CUSTOMER_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "Customer name is required"
            },
            "email": {
                "bsonType": ["string", "null"],
                "description": "Email address if provided"
            }
        }
    }
}

ORDER_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["customer_id", "items", "shipping_address", "subtotal", "status"],
        "properties": {
            "customer_id": {
                "bsonType": "objectId",
                "description": "Customer reference must be an ObjectId"
            },
            "items": {
                "bsonType": "array",
                "minItems": 1,
                "description": "Order must have at least one embedded item"
            },
            "subtotal": {
                "bsonType": ["double", "int", "decimal"],
                "minimum": 0,
                "description": "Subtotal must be non-negative"
            },
            "status": {
                "enum": ["pending", "confirmed", "shipped", "delivered", "cancelled"],
                "description": "Status must be pending, confirmed, shipped, delivered, or cancelled"
            }
        }
    }
}

REVIEW_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["product_id", "customer_id", "rating"],
        "properties": {
            "product_id": {
                "bsonType": "objectId",
                "description": "Reference to product ObjectId"
            },
            "customer_id": {
                "bsonType": "objectId",
                "description": "Reference to customer ObjectId"
            },
            "rating": {
                "bsonType": "int",
                "minimum": 1,
                "maximum": 5,
                "description": "Rating must be an integer between 1 and 5"
            }
        }
    }
}

DEMO_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["item_name", "price", "stock"],
        "properties": {
            "item_name": {
                "bsonType": "string",
                "description": "Item name is required string"
            },
            "price": {
                "bsonType": ["double", "int"],
                "minimum": 1.0,
                "description": "Price must be at least 1.0"
            },
            "stock": {
                "bsonType": "int",
                "minimum": 0,
                "description": "Stock must be non-negative integer"
            }
        }
    }
}

def apply_collection_validators(db: Database) -> None:
    """Apply schema validation to collections if they don't already exist or update them."""
    validators = {
        "products": PRODUCT_VALIDATOR,
        "customers": CUSTOMER_VALIDATOR,
        "orders": ORDER_VALIDATOR,
        "reviews": REVIEW_VALIDATOR,
        "shopsphere_demo": DEMO_VALIDATOR,
    }

    existing_collections = db.list_collection_names()
    for col_name, validator in validators.items():
        try:
            if col_name not in existing_collections:
                db.create_collection(col_name, validator=validator)
                logger.info(f"Created collection '{col_name}' with schema validator.")
            else:
                # Update existing collection validator
                db.command({
                    "collMod": col_name,
                    "validator": validator,
                    "validationLevel": "moderate"
                })
                logger.info(f"Updated schema validator for existing collection '{col_name}'.")
        except Exception as e:
            logger.warning(f"Could not apply validator for '{col_name}': {e}")
