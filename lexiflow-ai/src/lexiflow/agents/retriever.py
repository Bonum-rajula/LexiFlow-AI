# src/lexiflow/agents/retriever.py
from typing import Optional, Dict, Any
from loguru import logger

from ..core.interfaces import VectorStore, Embedder
from ..core.state import AgentState
from .base import format_chunks_for_prompt


class RetrieverAgent:
    """
    Agent A: Retrieves relevant document chunks for a given question.
    
    DIP Compliance: Depends on abstractions (VectorStore, Embedder), 
    NOT concrete implementations (ChromaDB, OpenAIEmbedder).
    """

    def __init__(
        self,
        vector_store: VectorStore,
        embedder: Embedder,
        top_k: int = 5,
    ):
        """
        Args:
            vector_store: Abstract vector database for similarity search.
            embedder: Abstract embedder for vectorizing queries.
            top_k: Number of chunks to retrieve.
        """
        self.vector_store = vector_store
        self.embedder = embedder
        self.top_k = top_k

    async def retrieve(self, state: AgentState) -> Dict[str, Any]:
        """
        Execute the retrieval pipeline.
        
        Args:
            state: Current agent state containing the user's question.
            
        Returns:
            Updated state fields: "chunks" and optionally "error".
        """
        question = state.get("question", "").strip()
        if not question:
            logger.error("Retriever received empty question.")
            return {"chunks": [], "error": "Empty question provided."}

        logger.info(f"🔍 Retriever: Searching for '{question[:50]}...'")

        try:
            # 1. Embed the question
            query_embedding = self.embedder.embed_query(question)
            
            # 2. Perform similarity search
            chunks = self.vector_store.similarity_search(
                query_embedding=query_embedding,
                k=self.top_k,
            )
            
            # 3. Log and return
            logger.info(f"✅ Retriever: Found {len(chunks)} chunks.")
            if chunks:
                preview = format_chunks_for_prompt(chunks)[:100]
                logger.debug(f"   Preview: {preview}...")
            
            return {
                "chunks": chunks,
                "error": None,  # Clear any previous errors
            }

        except Exception as e:
            logger.error(f"❌ Retriever failed: {str(e)}")
            return {
                "chunks": [],
                "error": f"Retrieval failed: {str(e)}",
            }