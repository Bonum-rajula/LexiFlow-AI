# src/lexiflow/infrastructure/vector_stores/chroma_store.py
import uuid
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings

from ...core.interfaces import VectorStore
from ...core.config import settings


class ChromaStore(VectorStore):
    """Concrete vector store using ChromaDB (HTTP client)."""

    def __init__(self):
        self.host = settings.chroma_host
        self.port = settings.chroma_port
        self.collection_name = settings.chroma_collection
        
        # Initialize HTTP client
        self.client = chromadb.HttpClient(
            host=self.host,
            port=self.port,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        
        # Get or create the collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},  # Cosine similarity
        )

    def add_documents(
        self,
        documents: List[Dict[str, Any]],
        embeddings: List[List[float]],
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """Add documents and their embeddings to the store."""
        if len(documents) != len(embeddings):
            raise ValueError("Number of documents must match number of embeddings.")
        
        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in range(len(documents))]
        elif len(ids) != len(documents):
            raise ValueError("Number of IDs must match number of documents.")
        
        # Extract texts and metadata
        texts = [doc["text"] for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]
        
        # Upsert into Chroma
        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        return ids

    def similarity_search(
        self,
        query_embedding: List[float],
        k: int = 5,
        filter_criteria: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieve top-k similar documents with optional metadata filters."""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=filter_criteria,  # Chroma uses 'where' for metadata filtering
            include=["documents", "metadatas", "distances"],
        )
        
        # Transform results into our standard format
        retrieved = []
        if results["documents"] and results["documents"][0]:
            for i, text in enumerate(results["documents"][0]):
                retrieved.append({
                    "text": text,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "score": 1 - results["distances"][0][i],  # Convert distance to similarity (cosine)
                })
        return retrieved

    def delete_collection(self) -> None:
        """Delete the entire collection."""
        self.client.delete_collection(self.collection_name)
        # Recreate it to keep the store usable
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )