import pytest
from pathlib import Path

@pytest.fixture
def sample_pdf_path():
    path = Path(__file__).parent.parent / "sample.pdf"
    if not path.exists():
        pytest.skip("sample.pdf not found in project root")
    return path