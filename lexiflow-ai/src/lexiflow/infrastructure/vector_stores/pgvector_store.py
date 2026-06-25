# src/lexiflow/infrastructure/vector_stores/pgvector_store.py
from typing import List, Dict, Any, Optional

from ...core.interfaces import VectorStore


class PGVectorStore(VectorStore):
    """Stub for future PostgreSQL + pgvector implementation."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        raise NotImplementedError(
            "PGVectorStore is a placeholder for future implementation. "
            "Use ChromaStore for now."
        )

    def add_documents(
        self,
        documents: List[Dict[str, Any]],
        embeddings: List[List[float]],
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        raise NotImplementedError

    def similarity_search(
        self,
        query_embedding: List[float],
        k: int = 5,
        filter_criteria: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def delete_collection(self) -> None:
        raise NotImplementedError