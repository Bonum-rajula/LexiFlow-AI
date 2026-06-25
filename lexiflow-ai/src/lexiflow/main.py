# src/lexiflow/main.py
from fastapi import FastAPI
from loguru import logger

from .core.config import settings
from .infrastructure import PyPDFParser, OpenAIEmbedder, ChromaStore, OpenAILLM
from .agents import RetrieverAgent, CriticAgent, SynthesizerAgent
from .orchestration import Orchestrator
from .services import IngestionService, QueryService

# Import the router objects AND the setter functions directly
from lexiflow.api.routes import (
    ingestion_router,
    query_router,
    set_ingestion_service,
    set_query_service,
)

# ------------------------------------------------------------
# 1. Application Factory & Dependency Injection (The Wiring)
# ------------------------------------------------------------

app = FastAPI(
    title="LexiFlow AI",
    description="Autonomous Multi-Agent RAG Orchestrator",
    version="0.1.0",
)

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
# 8. Health Check & Startup Events
# ------------------------------------------------------------

@app.on_event("startup")
async def startup_event():
    logger.info(f"🚀 LexiFlow AI starting with log level: {settings.log_level}")
    logger.info(f"🔗 Connecting to ChromaDB at: {settings.chroma_http_url}")

@app.get("/health")
async def health_check():
    return {"status": "alive", "vector_db": settings.chroma_http_url}

# For direct execution (optional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)