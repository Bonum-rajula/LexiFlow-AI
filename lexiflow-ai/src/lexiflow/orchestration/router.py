# src/lexiflow/orchestration/router.py
import json
from typing import Literal

from loguru import logger

from ..core.state import AgentState


def should_continue(state: AgentState) -> Literal["continue", "retry"]:
    """
    Conditional edge function for LangGraph.
    
    Determines whether to proceed to synthesis or loop back to retrieval
    based on the critic's evaluation and retry limits.
    
    Returns:
        "continue" → route to synthesizer
        "retry"    → route back to retriever
    """
    error = state.get("error")
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 2)
    critique_raw = state.get("critique", "")
    chunks = state.get("chunks", [])

    # 1. If there was a fatal error, skip retry and proceed to synthesis
    #    (so the user gets a graceful error message).
    if error:
        logger.info("⚠️ Router: Fatal error detected. Proceeding to synthesis with error message.")
        return "continue"

    # 2. If no chunks were retrieved, retry only if we haven't exhausted attempts.
    if not chunks:
        if retry_count < max_retries:
            logger.info(f"🔄 Router: No chunks (retry {retry_count+1}/{max_retries}). Looping back to Retriever.")
            return "retry"
        else:
            logger.warning("⛔ Router: Max retries reached with no chunks. Proceeding to synthesis with empty context.")
            return "continue"

    # 3. Parse the critique to check quality.
    try:
        if not critique_raw:
            # No critique means we can't evaluate quality; proceed safely.
            logger.info("🔀 Router: No critique available. Proceeding to synthesis.")
            return "continue"
        
        critique_data = json.loads(critique_raw)
        relevance_score = critique_data.get("relevance_score", 0.5)
        hallucination_risk = critique_data.get("hallucination_risk", "Medium")

        # 4. Decision logic: retry if relevance is low, risk is high, AND we haven't retried too much.
        if relevance_score < 0.4 or hallucination_risk == "High":
            if retry_count < max_retries:
                logger.info(
                    f"🔄 Router: Poor critique (score={relevance_score}, risk={hallucination_risk}). "
                    f"Looping back to Retriever ({retry_count+1}/{max_retries})."
                )
                return "retry"
            else:
                logger.warning(
                    f"⛔ Router: Max retries reached despite poor critique. "
                    f"Proceeding to synthesis with limitations."
                )
                return "continue"
        else:
            logger.info(f"✅ Router: Critique acceptable (score={relevance_score}). Proceeding to synthesis.")
            return "continue"

    except (json.JSONDecodeError, KeyError) as e:
        # If critique is malformed, proceed safely.
        logger.warning(f"⚠️ Router: Could not parse critique ({str(e)}). Proceeding to synthesis.")
        return "continue"