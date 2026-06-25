# src/lexiflow/api/schemas/requests.py
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """Request model for the /ask endpoint."""
    question: str = Field(..., description="The user's query", min_length=1, max_length=4096)

class UploadResponse(BaseModel):
    """Response model for the /upload endpoint."""
    filename: str
    num_chunks: int
    status: str
    message: str