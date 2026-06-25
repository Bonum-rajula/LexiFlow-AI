# src/lexiflow/core/interfaces/vector_store.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class VectorStore(ABC):
    """Abstract interface for vector database operations."""
    
    @abstractmethod
    def add_documents(
        self,
        documents: List[Dict[str, Any]],
        embeddings: List[List[float]],
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Store documents with their embeddings.
        
        Args:
            documents: List of dicts with "text" and "metadata" keys.
            embeddings: List of embedding vectors (aligned with documents).
            ids: Optional list of unique IDs. If None, generate automatically.
            
        Returns:
            List of stored IDs.
        """
        pass
    
    @abstractmethod
    def similarity_search(
        self,
        query_embedding: List[float],
        k: int = 5,
        filter_criteria: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve the top-k most similar documents.
        
        Args:
            query_embedding: The embedding vector of the query.
            k: Number of documents to retrieve.
            filter_criteria: Optional metadata filters (e.g., {"page": 1}).
            
        Returns:
            List of documents, each with "text", "metadata", and "score".
        """
        pass
    
    @abstractmethod
    def delete_collection(self) -> None:
        """Clear all documents from the collection."""
        pass