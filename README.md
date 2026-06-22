# LexiFlow AI: Autonomous Multi-Agent RAG Orchestrator

**Lightweight, open-source, multi-agent RAG for technical documents, built with Python, FastAPI, LangGraph, and vector search.**

LexiFlow AI is an autonomous document intelligence system designed to ingest dense technical PDFs, retrieve the most relevant context, critique retrieval quality, and synthesize grounded answers with a multi-agent workflow.

It is built for teams and engineers who need more than a basic chatbot: they need a reliable, inspectable, and modular assistant that can reason over long-form documents with better structure and control.

---

## Why LexiFlow AI Exists

Large technical PDFs are difficult to query well with a single-pass retrieval pipeline. LexiFlow AI addresses that with a layered agentic design:

- **Agent A — Retriever:** extracts and retrieves the most relevant chunks from the source document.
- **Agent B — Critic:** checks whether the retrieved context actually supports the user’s question and flags missing or weak evidence.
- **Agent C — Synthesizer:** generates a final answer grounded in the validated context.

This separation of concerns makes the system easier to debug, easier to extend, and more trustworthy for high-stakes technical reading.

---

## What Makes It Stand Out

- **Built around LangGraph** for explicit agent workflows and controlled orchestration.
- **Multi-agent reasoning pipeline** instead of a flat retrieve-and-generate chain.
- **RAG-first architecture** for grounded, document-based answers.
- **Designed for heavy PDFs** such as compliance manuals, policy documents, research papers, and technical standards.
- **Dockerized deployment** for repeatable local and production environments.
- **Vector database ready** with support for **ChromaDB** or **pgvector**.
- **FastAPI backend** for clean, modern API delivery.
- **Portfolio-friendly naming and structure** that clearly signals LangGraph experience to recruiters and technical reviewers.

---

## Tech Stack

**Core**
- Python
- FastAPI
- LangGraph
- LangChain

**Retrieval & Storage**
- ChromaDB or pgvector
- Embedding model of choice
- Document chunking and metadata storage

**Infrastructure**
- Docker
- Docker Compose

**Optional Enhancements**
- PostgreSQL
- OCR for scanned PDFs
- Streamlit or React frontend
- Background queue for ingestion jobs
- Authentication and usage tracking

---

## Architecture Overview

```text
User Query
   ↓
FastAPI Endpoint
   ↓
LangGraph Orchestrator
   ├── Agent A: Retrieve relevant chunks
   ├── Agent B: Critique factual grounding
   └── Agent C: Synthesize final answer
   ↓
Response with grounded context
```

### Agent Responsibilities

#### Agent A — Retriever
Fetches the most relevant chunks from the indexed document corpus using vector similarity search and metadata filters.

#### Agent B — Critic
Evaluates whether the retrieved context is sufficient, relevant, and factually aligned with the user query. It can request more evidence when needed.

#### Agent C — Synthesizer
Produces the final response from the validated context, keeping the answer concise, accurate, and grounded in source material.

---

## Key Features

- PDF upload and ingestion
- Text extraction and chunking
- Vector indexing
- Multi-agent query workflow
- Grounded response generation
- Retrieval critique step
- API-first design
- Dockerized deployment
- Extensible architecture for future agents and tools

---

## Example Use Cases

LexiFlow AI is ideal for:

- Compliance and policy document search
- Scientific paper question answering
- Internal knowledge base assistants
- Procurement and tender document review
- Technical manual navigation
- Research support for long-form PDFs

---

## Project Goals

LexiFlow AI was designed to demonstrate:

- Practical LangGraph implementation
- Strong backend engineering with FastAPI
- Production-minded retrieval architecture
- Modular system design
- Clear technical depth for AI automation roles

This makes the project especially relevant for roles involving:
- AI Automation Engineering
- LLM Application Development
- Retrieval-Augmented Generation
- Agentic workflow design
- Backend AI systems

---

## Repository Structure

```text
lexiflow-ai/
├── app/
│   ├── api/
│   ├── core/
│   ├── agents/
│   ├── rag/
│   ├── services/
│   └── main.py
├── data/
│   ├── uploads/
│   └── processed/
├── tests/
├── docker/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Docker and Docker Compose
- Git
- API key or local model access, depending on your LLM setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/lexiflow-ai.git
cd lexiflow-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
CHROMA_PERSIST_DIR=./data/chroma
UPLOAD_DIR=./data/uploads
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4.1-mini
```

If you are using PostgreSQL with pgvector, include:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/lexiflow
```

### 5. Run the app locally

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## Docker Setup

### Build and run

```bash
docker compose up --build
```

This starts the application in a reproducible containerized environment.

---

## API Endpoints

### Health Check

```http
GET /health
```

### Upload Document

```http
POST /documents/upload
```

### Ask a Question

```http
POST /query
```

Example payload:

```json
{
  "document_id": "doc_001",
  "question": "What does the policy say about data retention?"
}
```

### List Documents

```http
GET /documents
```

---

## Design Principles

### 1. Grounded Answers
The system prioritizes evidence-backed responses over fluent but unsupported generation.

### 2. Separation of Concerns
Retrieval, critique, and synthesis are handled by different nodes in the graph.

### 3. Modularity
Each component can be improved independently without rewriting the whole system.

### 4. Portability
Docker support makes it easy to run locally, in CI, or in a cloud environment.

### 5. Extensibility
The graph can later support memory, tool use, query routing, or human-in-the-loop review.

---

## Security and Reliability Notes

- Uploaded files should be validated before processing.
- Sensitive documents should be stored with access controls.
- API keys must never be committed to version control.
- Logging should avoid leaking source content unless intentionally enabled.
- OCR and ingestion pipelines should fail gracefully on malformed files.

---

## Roadmap

- Add OCR support for scanned PDFs
- Add citation-level source highlighting
- Add streaming responses
- Add authentication and rate limiting
- Add document-level permissions
- Add evaluation harness for retrieval accuracy
- Add web UI for document uploads and chat
- Add query routing across multiple documents

---

## Why Recruiters Notice This Project

LexiFlow AI is not just another chatbot clone. It signals:

- Real understanding of agent orchestration
- Strong backend API engineering
- Retrieval architecture knowledge
- Document AI experience
- Professional deployment awareness
- LangGraph experience made visible in the repo title

That makes it a strong portfolio piece for AI automation and LLM engineering roles.

---

## License

Open-source license placeholder. Add one that matches your intended distribution model.

---

## Author

Built by **Ranger** as a portfolio-grade demonstration of agentic RAG design, backend engineering, and practical AI system architecture.
