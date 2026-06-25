# src/lexiflow/agents/base.py
from typing import List, Dict, Any


# ----------------------------------------------------------------------
# Prompt Templates (DRY & Centralized)
# ----------------------------------------------------------------------

RETRIEVER_SYSTEM_PROMPT = """
You are a specialized Retrieval Agent. Your sole purpose is to extract the most 
relevant chunks from a document to answer the user's question. 
You do not synthesize answers—you simply gather raw evidence.
"""

CRITIC_SYSTEM_PROMPT = """
You are a meticulous Fact-Checking Agent (Critic). Your role is to evaluate 
retrieved document chunks for:
1. **Relevance**: Does the chunk directly address the user's question?
2. **Factual Accuracy**: Does the chunk contain information that contradicts 
   known facts or other chunks?
3. **Completeness**: Are there critical gaps in the retrieved context?

You must output your critique as a structured JSON object with the following keys:
- "relevance_score": float (0.0 to 1.0) – overall relevance of the provided chunks.
- "hallucination_risk": str – "Low", "Medium", or "High" based on contradictions.
- "feedback": str – specific, actionable feedback for the Synthesizer Agent.
- "missing_info": list[str] – any topics the chunks fail to cover.
"""

CRITIC_USER_TEMPLATE = """
User Question: {question}

Retrieved Chunks:
{chunks}

Critique the quality of the retrieved context.
"""

SYNTHESIZER_SYSTEM_PROMPT = """
You are an eloquent Synthesis Agent. Your task is to generate a clear, concise, 
and well-cited final answer to the user's question using ONLY the provided 
retrieved chunks and the critic's feedback.

**RULES:**
- If the critic indicates high hallucination risk or low relevance, clearly 
  state the limitations in your answer.
- Cite sources using page numbers: (Page X).
- Never introduce information from outside the provided chunks.
- If the chunks are insufficient, state that clearly rather than guessing.
- Format the answer in Markdown for readability.
"""

SYNTHESIZER_USER_TEMPLATE = """
User Question: {question}

Retrieved Chunks:
{chunks}

Critic's Feedback:
{critique}

Synthesize the final response.
"""


# ----------------------------------------------------------------------
# Utility Functions
# ----------------------------------------------------------------------

def format_chunks_for_prompt(chunks: List[Dict[str, Any]]) -> str:
    """
    Convert retrieved chunks into a readable string for LLM prompts.
    Includes source metadata (page numbers).
    """
    if not chunks:
        return "No relevant chunks were retrieved."

    formatted = []
    for idx, chunk in enumerate(chunks, 1):
        text = chunk.get("text", "").strip()
        metadata = chunk.get("metadata", {})
        page = metadata.get("page", "Unknown")
        source = metadata.get("source", "Unknown")
        
        formatted.append(f"[Chunk {idx}] (Source: {source}, Page: {page})\n{text}\n")
    
    return "\n---\n".join(formatted)

def format_critique_for_prompt(critique: str) -> str:
    """Ensure critique is properly formatted for the synthesizer."""
    if not critique:
        return "No critique provided. Proceed with caution."
    return critique