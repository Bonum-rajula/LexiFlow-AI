import pytest
from unittest.mock import AsyncMock, MagicMock
from lexiflow.agents import RetrieverAgent
from lexiflow.core.state import AgentState

@pytest.mark.asyncio
async def test_retriever_success():
    # Mock dependencies
    mock_vector_store = MagicMock()
    mock_vector_store.similarity_search.return_value = [
        {"text": "chunk1", "metadata": {"page": 1}, "score": 0.9}
    ]
    mock_embedder = MagicMock()
    mock_embedder.embed_query.return_value = [0.1, 0.2]

    agent = RetrieverAgent(vector_store=mock_vector_store, embedder=mock_embedder, top_k=1)

    state = AgentState(question="test?", chunks=[], critique=None, final_answer=None, error=None, retry_count=0, max_retries=2)
    result = await agent.retrieve(state)

    assert "chunks" in result
    assert len(result["chunks"]) == 1
    assert result["error"] is None
    mock_embedder.embed_query.assert_called_once_with("test?")
    mock_vector_store.similarity_search.assert_called_once()

@pytest.mark.asyncio
async def test_retriever_empty_question():
    mock_vector_store = MagicMock()
    mock_embedder = MagicMock()
    agent = RetrieverAgent(vector_store=mock_vector_store, embedder=mock_embedder)
    state = AgentState(question="", chunks=[], critique=None, final_answer=None, error=None, retry_count=0, max_retries=2)
    result = await agent.retrieve(state)
    assert result["chunks"] == []
    assert result["error"] == "Empty question provided."