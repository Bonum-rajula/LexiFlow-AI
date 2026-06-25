# src/lexiflow/services/query_service.py
from typing import Dict, Any
from loguru import logger

from ..orchestration import Orchestrator


class QueryService:
    """
    Orchestrates the query pipeline: Invoke the LangGraph workflow.
    
    DIP Compliance: Depends on the Orchestrator (which itself depends on abstractions).
    """

    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator

    async def ask(self, question: str) -> Dict[str, Any]:
        """
        Process a question through the multi-agent system.
        
        Args:
            question: User's question.
            
        Returns:
            Final state dict with answer, chunks, critique, etc.
        """
        logger.info(f"❓ QueryService: Processing question: '{question[:50]}...'")

        try:
            final_state = await self.orchestrator.run(question)
            logger.info("✅ QueryService: Workflow completed.")
            return final_state
        except Exception as e:
            logger.error(f"❌ QueryService failed: {str(e)}")
            # Return a graceful error state
            return {
                "question": question,
                "chunks": [],
                "critique": None,
                "final_answer": f"An error occurred while processing your request: {str(e)}",
                "error": str(e),
                "retry_count": 0,
                "max_retries": 0,
            }