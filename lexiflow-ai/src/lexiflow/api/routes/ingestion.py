# src/lexiflow/api/routes/ingestion.py
import tempfile
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from loguru import logger

from ...services.ingestion_service import IngestionService
from ..schemas.requests import UploadResponse

router = APIRouter(prefix="/upload", tags=["Ingestion"])

# Dependency injection: we'll provide the service via a factory in main.py
# For now, we'll use a global instance (will be set in main.py).
_ingestion_service: IngestionService = None

def set_ingestion_service(service: IngestionService):
    global _ingestion_service
    _ingestion_service = service

@router.post("/", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF document for ingestion into the vector store.
    """
    if not _ingestion_service:
        raise HTTPException(status_code=503, detail="Ingestion service not initialized")

    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Save the uploaded file to a temporary location
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = Path(tmp.name)

        # Ingest the file
        result = await _ingestion_service.ingest(tmp_path)

        # Clean up temporary file
        tmp_path.unlink(missing_ok=True)

        return UploadResponse(**result)

    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")