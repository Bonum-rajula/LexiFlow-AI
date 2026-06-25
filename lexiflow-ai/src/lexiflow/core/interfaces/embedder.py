# src/lexiflow/core/interfaces/embedder.py
from abc import ABC, abstractmethod
from typing import List


class Embedder(ABC):
    """Abstract interface for generating text embeddings."""
    
    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string (shorter, optimized for search)."""
        pass
    
    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a batch of document chunks."""
        pass
    
    @property
    @abstractmethod
    def embedding_dimension(self) -> int:
        """Return the dimensionality of the embedding vectors."""
        pass