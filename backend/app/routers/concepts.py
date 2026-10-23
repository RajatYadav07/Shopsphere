from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.database import Database

from app.core.database import get_db
from app.core.indexes import get_indexes_summary
from app.repositories.concepts_repository import ConceptsRepository
from app.schemas.common import APIResponse
from app.schemas.concepts import (
    AggregationPlaygroundRequest,
    AggregationPlaygroundResult,
    ConceptExecutionRequest,
    ConceptExecutionResult,
    ExplainQueryRequest,
    ExplainQueryResult,
    SchemaValidationDemoRequest,
    SchemaValidationDemoResult,
)

router = APIRouter(prefix="/concepts", tags=["MongoDB Concepts Lab"])

@router.post("/crud", response_model=APIResponse[ConceptExecutionResult])
def execute_crud_operation(req: ConceptExecutionRequest, db: Database = Depends(get_db)):
    repo = ConceptsRepository(db)
    try:
        res = repo.execute_crud_demo(req.operation, req.payload)
        return APIResponse(data=res)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/modeling", response_model=APIResponse[dict])
def get_data_modeling_comparison(db: Database = Depends(get_db)):
    repo = ConceptsRepository(db)
    res = repo.get_modeling_comparison()
    return APIResponse(data=res)

@router.post("/aggregation", response_model=APIResponse[AggregationPlaygroundResult])
def run_aggregation_pipeline(req: AggregationPlaygroundRequest, db: Database = Depends(get_db)):
    repo = ConceptsRepository(db)
    try:
        res = repo.run_aggregation_playground(req.query_id)
        return APIResponse(data=res)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Aggregation error: {str(e)}")

@router.post("/explain", response_model=APIResponse[ExplainQueryResult])
def explain_query(req: ExplainQueryRequest, db: Database = Depends(get_db)):
    repo = ConceptsRepository(db)
    try:
        res = repo.explain_query_execution(req.scenario, req.force_collscan)
        return APIResponse(data=res)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/validation", response_model=APIResponse[SchemaValidationDemoResult])
def test_schema_validation(req: SchemaValidationDemoRequest, db: Database = Depends(get_db)):
    repo = ConceptsRepository(db)
    res = repo.test_schema_validation(
        test_type=req.test_type,
        price=req.price or 25.0,
        stock=req.stock or 10,
        item_name=req.item_name or "Demo Mechanical Keyboard"
    )
    return APIResponse(data=res)

@router.get("/indexes", response_model=APIResponse[dict])
def list_database_indexes(db: Database = Depends(get_db)):
    summary = get_indexes_summary(db)
    return APIResponse(data=summary)
