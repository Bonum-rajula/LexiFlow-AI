# src/lexiflow/api/routes/query.py
from fastapi import APIRouter, HTTPException, Depends
from loguru import logger

from ...services.query_service import QueryService
from ..schemas.requests import AskRequest
from ..schemas.responses import AnswerResponse

router = APIRouter(prefix="/ask", tags=["Query"])

_query_service: QueryService = None

def set_query_service(service: QueryService):
    global _query_service
    _query_service = service

@router.post("/", response_model=AnswerResponse)
async def ask_question(request: AskRequest):
    """
    Ask a question using the multi-agent RAG system.
    """
    if not _query_service:
        raise HTTPException(status_code=503, detail="Query service not initialized")

    try:
        result = await _query_service.ask(request.question)
        return AnswerResponse(
            answer=result.get("final_answer", "No answer generated."),
            chunks_used=len(result.get("chunks", [])),
            critique=result.get("critique"),
            retry_count=result.get("retry_count", 0),
            error=result.get("error"),
        )
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process question: {str(e)}")