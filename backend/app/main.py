import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo.errors import ConnectionFailure, DuplicateKeyError, PyMongoError

from app.core.config import settings
from app.core.database import db_manager
from app.core.indexes import create_all_indexes
from app.core.validators import apply_collection_validators
from app.routers import (
    analytics,
    concepts,
    customers,
    dashboard,
    inventory,
    orders,
    products,
    reviews,
    settings as settings_router,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("shopsphere.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB and ensure indexes & validators
    logger.info("Initializing ShopSphere MongoDB connection...")
    try:
        db_manager.connect()
        db = db_manager.get_database()
        apply_collection_validators(db)
        create_all_indexes(db)
        logger.info("MongoDB initialized successfully with validators and indexes.")
    except Exception as e:
        logger.error(f"MongoDB startup initialization warning: {e}")
        logger.info("ShopSphere backend running; MongoDB endpoints will return connection errors if unavailable.")
    yield
    # Shutdown
    db_manager.close()
    logger.info("ShopSphere shutdown complete.")

app = FastAPI(
    title="ShopSphere API",
    description="ShopSphere E-Commerce & MongoDB Analytics Platform Backend. Provides real-time NoSQL queries, aggregations, query explain plans, and transactional order workflows.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS configuration
origins = settings.cors_origin_list
if "http://localhost:5173" not in origins:
    origins.append("http://localhost:5173")
if "http://127.0.0.1:5173" not in origins:
    origins.append("http://127.0.0.1:5173")

# Allow all origins if '*' is specified, or support preview domains dynamically
allow_all = "*" in origins or settings.ENVIRONMENT == "production"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all else origins,
    allow_credentials=True if not allow_all else False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Exception Handlers
@app.exception_handler(ConnectionFailure)
async def mongo_connection_exception_handler(request: Request, exc: ConnectionFailure):
    logger.error(f"MongoDB Connection Failure: {exc}")
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "success": False,
            "message": "MongoDB service is unreachable. Ensure MongoDB Community Server is running on port 27017.",
            "error": str(exc)
        }
    )

@app.exception_handler(DuplicateKeyError)
async def duplicate_key_exception_handler(request: Request, exc: DuplicateKeyError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "success": False,
            "message": "Duplicate key violation: a record with this unique identifier already exists in MongoDB.",
            "error": str(exc.details.get("errmsg") if hasattr(exc, "details") else exc)
        }
    )

# Include Routers
prefix = settings.API_V1_STR
app.include_router(dashboard.router, prefix=prefix)
app.include_router(products.router, prefix=prefix)
app.include_router(customers.router, prefix=prefix)
app.include_router(orders.router, prefix=prefix)
app.include_router(inventory.router, prefix=prefix)
app.include_router(reviews.router, prefix=prefix)
app.include_router(analytics.router, prefix=prefix)
app.include_router(concepts.router, prefix=prefix)
app.include_router(settings_router.router, prefix=prefix)

@app.get("/", tags=["Health"])
def root():
    return {
        "project": "ShopSphere",
        "description": "Premium E-Commerce & MongoDB Analytics Platform",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health"
    }

@app.get("/health", tags=["Health"])
def health_check():
    conn_info = db_manager.check_connection()
    return {
        "status": "healthy" if conn_info["connected"] else "degraded",
        "mongodb": conn_info
    }
