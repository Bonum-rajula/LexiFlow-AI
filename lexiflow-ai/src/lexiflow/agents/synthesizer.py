# src/lexiflow/agents/synthesizer.py
import json
from typing import Dict, Any

from loguru import logger

from ..core.interfaces import LLMProvider
from ..core.state import AgentState
from .base import (
    SYNTHESIZER_SYSTEM_PROMPT,
    SYNTHESIZER_USER_TEMPLATE,
    format_chunks_for_prompt,
    format_critique_for_prompt,
)


class SynthesizerAgent:
    """
    Agent C: Synthesizes the final answer from retrieved chunks and critique.
    
    DIP Compliance: Depends only on LLMProvider abstraction.
    """

    def __init__(self, llm: LLMProvider):
        """Args: llm: Abstract LLM provider for generating the final answer."""
        self.llm = llm

    async def synthesize(self, state: AgentState) -> Dict[str, Any]:
        """
        Execute the synthesis pipeline.
        
        Args:
            state: Current state with question, chunks, and critique.
            
        Returns:
            Updated state field: "final_answer".
        """
        question = state.get("question", "").strip()
        chunks = state.get("chunks", [])
        critique = state.get("critique", "")
        error = state.get("error")

        if error:
            logger.warning(f"Synthesizer: Skipping due to previous error: {error}")
            return {
                "final_answer": (
                    f"I encountered an error during processing: {error}\n\n"
                    "Please try rephrasing your question or uploading the document again."
                )
            }

        if not question:
            return {"final_answer": "No question provided."}

        logger.info("✍️ Synthesizer: Generating final answer...")

        try:
            formatted_chunks = format_chunks_for_prompt(chunks)
            formatted_critique = format_critique_for_prompt(critique)

            # If no chunks, guide the LLM to be transparent
            if not chunks:
                logger.warning("Synthesizer: No chunks available. Answering with disclaimer.")
                return {
                    "final_answer": (
                        "I couldn't find any relevant information in the document to answer "
                        "your question. Please ensure the document contains related content "
                        "or rephrase your question."
                    )
                }

            user_prompt = SYNTHESIZER_USER_TEMPLATE.format(
                question=question,
                chunks=formatted_chunks,
                critique=formatted_critique,
            )

            # Generate the final answer (plain text markdown)
            final_answer = self.llm.generate(
                prompt=user_prompt,
                system_prompt=SYNTHESIZER_SYSTEM_PROMPT,
                temperature=0.2,  # Slight creativity for fluent prose
            )

            logger.info("✅ Synthesizer: Final answer generated.")
            logger.debug(f"   Answer preview: {final_answer[:150]}...")

            return {"final_answer": final_answer}

        except Exception as e:
            logger.error(f"❌ Synthesizer failed: {str(e)}")
            return {
                "final_answer": (
                    f"I encountered an error while generating the answer: {str(e)}\n\n"
                    "Please try again or contact support if the issue persists."
                )
            }