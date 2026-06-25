# tests/integration/test_orchestration.py
import pytest
from pathlib import Path
from lexiflow.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.mark.integration
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"

@pytest.mark.integration
def test_upload_and_ask(tmp_path):
    # Create a simple PDF (or use a fixture) - skip if no sample.pdf
    pdf_path = Path(__file__).parent.parent.parent / "sample.pdf"
    if not pdf_path.exists():
        pytest.skip("sample.pdf not found")
    
    with open(pdf_path, "rb") as f:
        response = client.post("/upload/", files={"file": ("test.pdf", f, "application/pdf")})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["num_chunks"] > 0

    # Now ask a question
    response = client.post("/ask/", json={"question": "What is the main topic?"})
    assert response.status_code == 200
    answer_data = response.json()
    assert "answer" in answer_data
    assert len(answer_data["answer"]) > 0
    # Optionally, check that critique is present