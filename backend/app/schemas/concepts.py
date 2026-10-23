from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ConceptExecutionRequest(BaseModel):
    operation: str = Field(..., description="Operation identifier (e.g., 'insert_one', 'update_many')")
    payload: Optional[Dict[str, Any]] = Field(default_factory=dict)

class ConceptExecutionResult(BaseModel):
    operation: str
    mongo_code: str
    explanation: str
    execution_time_ms: float
    result: Any
    affected_count: Optional[int] = 0

class AggregationPlaygroundRequest(BaseModel):
    query_id: str = Field(..., description="Preset pipeline identifier (1 to 8)")

class AggregationPlaygroundResult(BaseModel):
    query_id: str
    title: str
    description: str
    stages_used: List[str]
    pipeline_code: str
    execution_time_ms: float
    result: List[Any]
    explanation: str

class ExplainQueryRequest(BaseModel):
    scenario: str = Field(default="find_by_sku", description="'find_by_sku' or 'category_price_filter' or 'customer_orders'")
    force_collscan: bool = Field(default=False, description="Whether to simulate a collection scan (e.g. via $natural hint)")

class ExplainQueryResult(BaseModel):
    scenario: str
    query_filter: Dict[str, Any]
    index_used: Optional[str]
    stage: str # IXSCAN or COLLSCAN
    nReturned: int
    totalKeysExamined: int
    totalDocsExamined: int
    executionTimeMillis: float
    is_index_scan: bool
    explanation: str
    raw_stats: Dict[str, Any]

class SchemaValidationDemoRequest(BaseModel):
    test_type: str = Field(..., description="'valid' or 'invalid'")
    price: Optional[float] = 25.0
    stock: Optional[int] = 10
    item_name: Optional[str] = "Demo Mechanical Keyboard"

class SchemaValidationDemoResult(BaseModel):
    test_type: str
    document_attempted: Dict[str, Any]
    accepted: bool
    status_message: str
    mongodb_error: Optional[str] = None
    explanation: str
