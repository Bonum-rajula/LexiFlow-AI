# src/lexiflow/main.py
from fastapi import FastAPI
from loguru import logger
from .core.config import settings

# Instantiate the app
app = FastAPI(
    title="LexiFlow AI",
    description="Autonomous Multi-Agent RAG Orchestrator",
    version="0.1.0",
)

@app.on_event("startup")
async def startup_event():
    logger.info(f"🚀 LexiFlow AI starting with log level: {settings.log_level}")
    logger.info(f"🔗 Connecting to ChromaDB at: {settings.chroma_http_url}")

@app.get("/health")
async def health_check():
    return {"status": "alive", "vector_db": settings.chroma_http_url}