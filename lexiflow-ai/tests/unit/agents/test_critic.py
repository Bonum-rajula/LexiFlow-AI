import json
import pytest
from unittest.mock import AsyncMock, MagicMock
from lexiflow.agents import CriticAgent
from lexiflow.core.state import AgentState

@pytest.mark.asyncio
async def test_critic_success():
    mock_llm = MagicMock()
    mock_llm.generate_with_json.return_value = {
        "relevance_score": 0.8,
        "hallucination_risk": "Low",
        "feedback": "Good chunks",
        "missing_info": []
    }
    agent = CriticAgent(llm=mock_llm)
    state = AgentState(
        question="test?",
        chunks=[{"text": "test chunk", "metadata": {"page": 1}}],
        critique=None,
        final_answer=None,
        error=None,
        retry_count=0,
        max_retries=2
    )
    result = await agent.critique(state)
    critique_data = json.loads(result["critique"])
    assert critique_data["relevance_score"] == 0.8