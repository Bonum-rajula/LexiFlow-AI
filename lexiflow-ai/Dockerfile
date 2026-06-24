# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (for PyMuPDF and Chroma)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy only the dependency file first (Docker layer caching)
COPY pyproject.toml ./

# Install dependencies using pip (since we don't have uv installed yet, pip is fine)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e . && \
    pip install --no-cache-dir pytest pytest-asyncio httpx

# Copy the rest of the source
COPY src/ ./src/
COPY tests/ ./tests/

# Run as non-root user
RUN useradd -m -u 1000 lexiflow && chown -R lexiflow:lexiflow /app
USER lexiflow

# Expose port
EXPOSE 8000

# The command is defined in docker-compose.yml