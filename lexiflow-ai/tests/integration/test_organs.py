# tests/integration/test_organs.py
import sys
from pathlib import Path

# Ensure src is in path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "sample.pdf"))

import pytest
from loguru import logger

from lexiflow.infrastructure import PyPDFParser, OpenAIEmbedder, ChromaStore
from lexiflow.core import settings


@pytest.fixture
def sample_pdf_path():
    """Path to a sample PDF for testing. You must provide one."""
    path = Path(__file__).parent.parent.parent / "sample.pdf"
    print(path)
    if not path.exists():
        pytest.skip("sample.pdf not found in project root. Please add one.")
    return path


def test_full_ingestion_pipeline(sample_pdf_path):
    """Integration test: Parse -> Embed -> Store -> Query."""
    logger.info("🧪 Phase 2 Integration Test: Full Ingestion Pipeline")

    # 1. Parse
    parser = PyPDFParser()
    chunks = parser.parse(sample_pdf_path)
    assert len(chunks) > 0, "No chunks extracted from PDF"
    logger.info(f"✅ Parsed {len(chunks)} chunks")

    # 2. Embed
    embedder = OpenAIEmbedder()
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedder.embed_documents(texts)
    assert len(embeddings) == len(chunks), "Embedding count mismatch"
    assert len(embeddings[0]) == embedder.embedding_dimension, "Embedding dimension mismatch"
    logger.info(f"✅ Embedded {len(embeddings)} chunks")

    # 3. Store
    store = ChromaStore()
    store.delete_collection()  # Fresh start
    ids = store.add_documents(chunks, embeddings)
    assert len(ids) == len(chunks), "Storage count mismatch"
    logger.info(f"✅ Stored {len(ids)} documents")

    # 4. Query
    query = "What is the main topic?"
    query_embedding = embedder.embed_query(query)
    results = store.similarity_search(query_embedding, k=3)
    assert len(results) > 0, "Query returned no results"
    
    # 5. Validate scores
    for res in results:
        assert 0 <= res["score"] <= 1, "Score out of range"
        assert "text" in res, "Missing text field"
    
    logger.success("🎉 All organs are functioning correctly.")