# src/lexiflow/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger

from .core.config import settings
from .infrastructure import PyPDFParser, OpenAIEmbedder, ChromaStore, OpenAILLM
from .agents import RetrieverAgent, CriticAgent, SynthesizerAgent
from .orchestration import Orchestrator
from .services import IngestionService, QueryService
from .middleware.logging_middleware import LoggingMiddleware

# Import the router objects AND the setter functions directly
from lexiflow.api.routes import (
    ingestion_router,
    query_router,
    set_ingestion_service,
    set_query_service,
)

# ------------------------------------------------------------
# Lifespan Events (replaces @app.on_event("startup"))
# ------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info(f"🚀 LexiFlow AI starting with log level: {settings.log_level}")
    logger.info(f"🔗 Connecting to ChromaDB at: {settings.chroma_http_url}")
    yield
    # Shutdown logic (if needed)
    logger.info("🛑 LexiFlow AI shutting down")

# ------------------------------------------------------------
# 1. Application Factory & Dependency Injection (The Wiring)
# ------------------------------------------------------------
app = FastAPI(
    title="LexiFlow AI",
    description="Autonomous Multi-Agent RAG Orchestrator",
    version="0.1.0",
    lifespan=lifespan,  # <-- attach the lifespan
)

# Add logging middleware first (optional, but good practice)
app.add_middleware(LoggingMiddleware)

# 2. Infrastructure layer (concrete implementations)
parser = PyPDFParser()
embedder = OpenAIEmbedder()
vector_store = ChromaStore()
llm = OpenAILLM()

# 3. Agents (injected with dependencies)
retriever = RetrieverAgent(vector_store=vector_store, embedder=embedder)
critic = CriticAgent(llm=llm)
synthesizer = SynthesizerAgent(llm=llm)

# 4. Orchestrator
orchestrator = Orchestrator(
    retriever=retriever,
    critic=critic,
    synthesizer=synthesizer,
    max_retries=2,
)

# 5. Services (injected with dependencies)
ingestion_service = IngestionService(
    parser=parser,
    embedder=embedder,
    vector_store=vector_store,
)
query_service = QueryService(orchestrator=orchestrator)

# 6. Inject services into route handlers (using the imported setter functions)
set_ingestion_service(ingestion_service)
set_query_service(query_service)

# 7. Register routers (using the imported router objects)
app.include_router(ingestion_router)
app.include_router(query_router)

# ------------------------------------------------------------
# 8. Health Check & Additional Endpoints
# ------------------------------------------------------------
@app.get("/health")
async def health_check():
    return {"status": "alive", "vector_db": settings.chroma_http_url}

@app.get("/health/details")
async def detailed_health():
    """
    Detailed health check that verifies connectivity to external dependencies.
    """
    status = {
        "api": "ok",
        "chroma": "unknown",
        "redis": "unknown",  # Redis not yet used, but we keep the field
        "llm": "ok",         # LLM is stateless, we assume it's ok
    }
    # Check ChromaDB connectivity by attempting to list collections
    try:
        # The ChromaStore instance is in the closure; we can access it directly.
        # We'll use a simple ping: get collection count or similar.
        # For ChromaDB HTTP client, we can try to list collections.
        collections = vector_store.client.list_collections()
        status["chroma"] = "ok" if collections is not None else "error"
    except Exception as e:
        logger.warning(f"ChromaDB health check failed: {e}")
        status["chroma"] = "error"

    # Redis is not yet used, but if we add it later, we can check it here.
    # For now, we just mark it as "not_configured"
    status["redis"] = "not_configured"

    return status

# For direct execution (optional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)