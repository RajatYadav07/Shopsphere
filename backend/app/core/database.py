import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from bson import ObjectId
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from app.core.config import settings

logger = logging.getLogger("shopsphere.database")

class DatabaseManager:
    client: Optional[MongoClient] = None
    db: Optional[Database] = None

    def connect(self) -> None:
        """Establish connection to MongoDB with timeout."""
        try:
            logger.info(f"Connecting to MongoDB at {settings.MONGODB_URI}")
            self.client = MongoClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=3000,
                connectTimeoutMS=3000,
                socketTimeoutMS=5000,
                retryWrites=True,
            )
            # Trigger connection check
            self.client.admin.command("ping")
            self.db = self.client[settings.DATABASE_NAME]
            logger.info(f"Successfully connected to MongoDB database '{settings.DATABASE_NAME}'")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            self.client = None
            self.db = None
            raise ConnectionFailure(
                f"Cannot connect to MongoDB at {settings.MONGODB_URI}. "
                f"Ensure MongoDB Community Server is installed and running on port 27017. Details: {e}"
            )

    def close(self) -> None:
        """Close connection cleanly."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")
            self.client = None
            self.db = None

    def get_database(self) -> Database:
        """Return database instance or raise descriptive error."""
        if self.db is None:
            self.connect()
        return self.db

    def check_connection(self) -> Dict[str, Any]:
        """Verify MongoDB health and report server details."""
        if not self.client:
            try:
                self.connect()
            except Exception as e:
                return {
                    "connected": False,
                    "error": str(e),
                    "database": settings.DATABASE_NAME,
                    "server_version": None,
                    "transactions_supported": False,
                    "topology": "unknown",
                }

        try:
            server_info = self.client.server_info()
            topology = self.client.topology_description.topology_type_name
            # In MongoDB, multi-document transactions require a replica set or sharded cluster.
            # Standalone single nodes (default Community Server installation on Windows) do not support transactions.
            is_replica_set = topology in ("ReplicaSetWithPrimary", "ReplicaSetNoPrimary", "Sharded")
            return {
                "connected": True,
                "error": None,
                "database": settings.DATABASE_NAME,
                "server_version": server_info.get("version"),
                "topology": topology,
                "transactions_supported": is_replica_set,
                "collections": self.db.list_collection_names() if self.db is not None else [],
            }
        except Exception as e:
            return {
                "connected": False,
                "error": str(e),
                "database": settings.DATABASE_NAME,
                "server_version": None,
                "transactions_supported": False,
                "topology": "unknown",
            }

db_manager = DatabaseManager()

def get_db() -> Database:
    """FastAPI Dependency for database access."""
    return db_manager.get_database()

def utc_now() -> datetime:
    """Return current UTC timestamp with timezone."""
    return datetime.now(timezone.utc)

def serialize_doc(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Recursively serialize BSON ObjectId and datetime to JSON-compatible types."""
    if doc is None:
        return None
    res = {}
    for key, value in doc.items():
        if key == "_id" and isinstance(value, ObjectId):
            res["id"] = str(value)
            res["_id"] = str(value)
        elif isinstance(value, ObjectId):
            res[key] = str(value)
        elif isinstance(value, datetime):
            res[key] = value.isoformat()
        elif isinstance(value, list):
            res[key] = [
                serialize_doc(item) if isinstance(item, dict)
                else str(item) if isinstance(item, ObjectId)
                else item.isoformat() if isinstance(item, datetime)
                else item
                for item in value
            ]
        elif isinstance(value, dict):
            res[key] = serialize_doc(value)
        else:
            res[key] = value
    return res

def serialize_docs(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Serialize list of BSON documents."""
    return [serialize_doc(d) for d in docs if d is not None]
