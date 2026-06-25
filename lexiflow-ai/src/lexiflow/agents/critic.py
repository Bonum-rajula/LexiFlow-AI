# src/lexiflow/agents/critic.py
import json
from typing import Dict, Any

from loguru import logger

from ..core.interfaces import LLMProvider
from ..core.state import AgentState
from .base import (
    CRITIC_SYSTEM_PROMPT,
    CRITIC_USER_TEMPLATE,
    format_chunks_for_prompt,
)


class CriticAgent:
    """
    Agent B: Critiques the quality of retrieved chunks for factual accuracy 
    and relevance.
    
    DIP Compliance: Depends only on LLMProvider abstraction.
    """

    def __init__(self, llm: LLMProvider):
        """Args: llm: Abstract LLM provider for generating critiques."""
        self.llm = llm

    async def critique(self, state: AgentState) -> Dict[str, Any]:
        """
        Execute the critique pipeline.
        
        Args:
            state: Current state with question and retrieved chunks.
            
        Returns:
            Updated state field: "critique" (formatted string).
        """
        question = state.get("question", "").strip()
        chunks = state.get("chunks", [])
        error = state.get("error")

        # If there was an error in retrieval, propagate it.
        if error:
            logger.warning(f"Critic: Skipping due to previous error: {error}")
            return {"critique": f"Critique skipped due to retrieval error: {error}"}

        if not question:
            return {"critique": "No question provided to critique."}

        if not chunks:
            logger.warning("Critic: No chunks to evaluate.")
            return {
                "critique": json.dumps({
                    "relevance_score": 0.0,
                    "hallucination_risk": "High",
                    "feedback": "No relevant chunks were retrieved. Cannot synthesize a factual answer.",
                    "missing_info": ["All topics"],
                })
            }

        logger.info(f"🧐 Critic: Evaluating {len(chunks)} chunks...")

        try:
            # Format chunks for the prompt
            formatted_chunks = format_chunks_for_prompt(chunks)
            user_prompt = CRITIC_USER_TEMPLATE.format(
                question=question,
                chunks=formatted_chunks,
            )

            # Generate JSON critique
            critique_json = self.llm.generate_with_json(
                prompt=user_prompt,
                system_prompt=CRITIC_SYSTEM_PROMPT,
                temperature=0.0,  # Deterministic for consistency
            )

            # Convert to string for storage in state
            critique_str = json.dumps(critique_json, indent=2)
            logger.info(f"✅ Critic: Score={critique_json.get('relevance_score', 0)}")

            return {"critique": critique_str}

        except Exception as e:
            logger.error(f"❌ Critic failed: {str(e)}")
            # Fallback critique
            fallback = {
                "relevance_score": 0.5,
                "hallucination_risk": "Medium",
                "feedback": f"Critique generation failed: {str(e)}. Proceed with caution.",
                "missing_info": ["Unable to determine"],
            }
            return {"critique": json.dumps(fallback)}