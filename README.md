# LexiFlow AI

## Autonomous Multi-Agent RAG Orchestrator

LexiFlow AI is a production-ready, open-source Retrieval-Augmented Generation (RAG) platform that leverages a multi-agent architecture to answer questions from complex technical documents with improved accuracy, traceability, and reliability.

Unlike traditional RAG pipelines that rely on a single retrieval-and-generation workflow, LexiFlow delegates responsibilities to specialized agents that collaborate through a stateful orchestration layer powered by LangGraph.

### Core Agents

* **Retriever Agent** — Retrieves the most relevant document chunks from a vector database.
* **Critic Agent** — Evaluates retrieved context for relevance, completeness, and factual consistency.
* **Synthesizer Agent** — Generates a final response using validated context and critique feedback.

The platform is built around the principles of Clean Architecture and Dependency Inversion, enabling developers to replace infrastructure components such as language models, vector stores, or embedding providers without modifying business logic.

---

## Key Features

### Multi-Agent Orchestration

Leverages LangGraph to coordinate specialized agents through stateful and conditional workflows.

### Intelligent Document Retrieval

Uses vector similarity search through ChromaDB to locate highly relevant contextual information.

### Automated Context Evaluation

A dedicated Critic Agent assesses retrieval quality and identifies gaps before answer generation.

### Self-Correcting Retrieval Loops

Automatically performs retrieval retries when context quality falls below acceptable thresholds.

### PDF Knowledge Ingestion

Uploads, parses, chunks, embeds, and indexes PDF documents for semantic search.

### Production-Oriented Design

Built with structured logging, health monitoring, resilience patterns, dependency injection, and automated testing.

### Containerized Deployment

Fully containerized using Docker and Docker Compose for reproducible local and production deployments.

---

## Architecture Overview

```text
User
 │
 ▼
┌─────────────────────────────────────────────────────────────────┐
│                        FastAPI Gateway                         │
│  /upload   (ingest PDFs)   │   /ask   (ask questions)          │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LangGraph Orchestrator                      │
│                                                               │
│  START                                                        │
│    │                                                          │
│    ▼                                                          │
│ Retriever Agent                                               │
│    │                                                          │
│    ▼                                                          │
│ Critic Agent                                                  │
│    │                                                          │
│    ▼                                                          │
│ Synthesizer Agent                                             │
│    │                                                          │
│    ▼                                                          │
│ Final Response                                                │
│                                                               │
│ Retriever → ChromaDB                                          │
│ Critic → LLM Provider                                         │
│ Synthesizer → LLM Provider                                    │
└───────────────────────────────────────────────────────────────┘
```

### Architectural Principles

LexiFlow follows a layered architecture:

* Domain and business logic remain independent of infrastructure concerns.
* Infrastructure dependencies are injected at runtime.
* Interfaces define contracts between layers.
* Components remain highly testable and replaceable.

---

## Technology Stack

| Layer                  | Technology                    |
| ---------------------- | ----------------------------- |
| API Framework          | FastAPI                       |
| Workflow Orchestration | LangGraph                     |
| Vector Database        | ChromaDB                      |
| Embeddings             | OpenAI text-embedding-3-small |
| Language Model         | OpenAI GPT-4o Mini            |
| PDF Processing         | PyMuPDF                       |
| Text Chunking          | LangChain Text Splitters      |
| Configuration          | Pydantic Settings             |
| Logging                | Loguru                        |
| Resilience             | Tenacity                      |
| Testing                | Pytest, Pytest-Asyncio, HTTPX |
| Containerization       | Docker, Docker Compose        |

---

## Getting Started

### Prerequisites

Before running the project, ensure the following tools are installed:

* Docker
* Docker Compose
* OpenAI API Key

---

### Clone the Repository

```bash
git clone https://github.com/yourusername/lexiflow-ai.git
cd lexiflow-ai
```

---

### Configure Environment Variables

Create a local environment file:

```bash
cp .env.example .env
```

Update the values accordingly:

```env
OPENAI_API_KEY=your_api_key

OPENAI_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

CHROMA_HTTP_URL=http://chromadb:8000

CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

---

### Build and Start Services

```bash
docker compose build
docker compose up -d
```

Services:

| Service          | URL                   |
| ---------------- | --------------------- |
| LexiFlow API     | http://localhost:8000 |
| ChromaDB         | http://localhost:8001 |
| Redis (Optional) | localhost:6380        |

---

### Verify Installation

```bash
curl http://localhost:8000/health
```

Example response:

```json
{
  "status": "alive",
  "vector_db": "http://chromadb:8000"
}
```

---

## API Usage

### Upload a PDF

```bash
curl -X POST http://localhost:8000/upload/ \
  -F "file=@/path/to/document.pdf"
```

Example response:

```json
{
  "filename": "document.pdf",
  "num_chunks": 42,
  "status": "success",
  "message": "Successfully ingested 42 chunks."
}
```

---

### Ask a Question

```bash
curl -X POST http://localhost:8000/ask/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What does section 3.2 say about data privacy?"
  }'
```

Example response:

```json
{
  "answer": "Section 3.2 states that all personal data must be anonymized before processing.",
  "chunks_used": 5,
  "critique": "{...}",
  "retry_count": 0,
  "error": null
}
```

---

## API Documentation

Interactive API documentation is automatically generated by FastAPI.

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

---

## Testing

### Unit Tests

```bash
docker exec -it lexiflow-api pytest tests/unit -v
```

### Integration Tests

```bash
docker exec -it lexiflow-api pytest tests/integration -v
```

### Test Coverage Goals

* Agent behavior
* Orchestrator workflows
* Service layer logic
* API endpoints
* Infrastructure adapters
* End-to-end document ingestion and querying

---

## Project Structure

```text
lexiflow-ai/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── .env.example
├── tests/
│   ├── unit/
│   └── integration/
│
└── src/
    └── lexiflow/
        ├── core/
        │   ├── interfaces/
        │   ├── state/
        │   └── config/
        │
        ├── infrastructure/
        │   ├── vectorstores/
        │   ├── embeddings/
        │   ├── llm/
        │   └── parsers/
        │
        ├── agents/
        │   ├── retriever/
        │   ├── critic/
        │   └── synthesizer/
        │
        ├── orchestration/
        │   └── graph.py
        │
        ├── services/
        │
        ├── api/
        │   ├── routes/
        │   └── schemas/
        │
        ├── middleware/
        │
        └── main.py
```

---

## Extending LexiFlow

### Add a New Agent

1. Create a new agent implementation.
2. Define the agent contract.
3. Register the node in the LangGraph workflow.
4. Add routing logic within the orchestrator.

### Replace the Vector Database

Implement the VectorStore interface and register the new implementation through dependency injection.

### Use a Different LLM Provider

Implement the LLMProvider abstraction for providers such as:

* Anthropic Claude
* Azure OpenAI
* Google Gemini
* Ollama
* Local LLMs

No business logic changes are required.

---

## Deployment Considerations

### Environment Management

Store sensitive configuration through environment variables or secret management systems.

### Horizontal Scaling

The API service remains stateless and can be scaled behind a load balancer.

### Persistent Storage

For production deployments:

* Persist ChromaDB storage volumes.
* Configure backup strategies.
* Deploy Redis as a managed service when applicable.

### Security

Before public exposure, consider implementing:

* API authentication
* Rate limiting
* Request validation policies
* TLS termination
* Audit logging

---

## Contributing

Contributions are welcome.

### Development Workflow

```bash
git checkout -b feature/my-feature
```

Implement your changes, add tests, and verify:

```bash
pytest tests/
```

Submit a Pull Request with:

* Clear description
* Architecture rationale
* Test coverage
* Documentation updates

---

## License

This project is licensed under the Apache License Version 2.0

See the LICENSE file for full details.

---

## Acknowledgments

LexiFlow AI is built upon several outstanding open-source technologies:

* LangGraph
* LangChain
* FastAPI
* ChromaDB
* OpenAI
* Pydantic
* PyMuPDF

Their contributions make modern AI application development significantly more accessible and maintainable.

---

## Author

**Bonum Rajula**

Email: [bonumrajula01@gmail.com](mailto:bonumrajula01@gmail.com)

GitHub: https://github.com/Bonum-rajula

---

LexiFlow AI demonstrates how autonomous multi-agent systems, clean architecture principles, and modern AI tooling can be combined to create reliable, extensible, and production-ready Retrieval-Augmented Generation platforms.
