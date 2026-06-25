# src/lexiflow/api/schemas/responses.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class AnswerResponse(BaseModel):
    """Response model for the /ask endpoint."""
    answer: str
    chunks_used: int
    critique: Optional[str] = None
    retry_count: int = 0
    error: Optional[str] = None

class HealthResponse(BaseModel):
    """Response model for the /health endpoint."""
    status: str
    vector_db: str
    version: str = "0.1.0"