# src/lexiflow/api/routes/__init__.py
from .ingestion import router as ingestion_router, set_ingestion_service
from .query import router as query_router, set_query_service

__all__ = [
    "ingestion_router", 
    "query_router", 
    "set_ingestion_service", 
    "set_query_service"
]