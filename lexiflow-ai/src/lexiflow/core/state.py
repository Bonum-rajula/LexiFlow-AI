# src/lexiflow/core/state.py
from typing import TypedDict, Optional, List, Dict, Any


class AgentState(TypedDict):
    """Shared state passed between agents in the LangGraph workflow."""
    
    # Input from the user
    question: str
    
    # Agent A (Retriever) output
    chunks: List[Dict[str, Any]]  # Each dict: {"text": str, "metadata": {"page": int, "source": str}}
    
    # Agent B (Critic) output
    critique: Optional[str]  # Detailed feedback on chunk relevance/factual accuracy
    
    # Agent C (Synthesizer) output
    final_answer: Optional[str]  # The final markdown response with citations
    
    # Error handling (for resilience)
    error: Optional[str]