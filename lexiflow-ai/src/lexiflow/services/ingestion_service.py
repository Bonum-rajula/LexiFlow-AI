# src/lexiflow/services/ingestion_service.py
from pathlib import Path
from typing import List, Dict, Any
from loguru import logger

from ..core.interfaces import DocumentParser, Embedder, VectorStore


class IngestionService:
    """
    Orchestrates the ingestion pipeline: Parse → Embed → Store.
    
    DIP Compliance: Depends on abstractions (DocumentParser, Embedder, VectorStore).
    No knowledge of concrete implementations.
    """

    def __init__(
        self,
        parser: DocumentParser,
        embedder: Embedder,
        vector_store: VectorStore,
    ):
        self.parser = parser
        self.embedder = embedder
        self.vector_store = vector_store

    async def ingest(self, file_path: Path) -> Dict[str, Any]:
        """
        Process a document and add it to the vector store.
        
        Args:
            file_path: Path to the document (PDF, etc.).
            
        Returns:
            Dict with status, chunk count, and metadata.
        """
        logger.info(f"📥 IngestionService: Processing {file_path.name}")

        # 1. Parse the document into chunks
        chunks = self.parser.parse(file_path)
        if not chunks:
            raise ValueError(f"No text extracted from {file_path.name}")
        logger.info(f"   Parsed {len(chunks)} chunks")

        # 2. Embed the chunks
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedder.embed_documents(texts)
        logger.info(f"   Embedded {len(embeddings)} chunks")

        # 3. Store in vector database
        ids = self.vector_store.add_documents(chunks, embeddings)
        logger.info(f"   Stored {len(ids)} documents")

        return {
            "filename": file_path.name,
            "num_chunks": len(chunks),
            "status": "success",
            "message": f"Successfully ingested {len(chunks)} chunks.",
        }