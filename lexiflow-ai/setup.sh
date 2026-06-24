#!/usr/bin/bash
# Create the src layout (as per our blueprint)
mkdir -p src/lexiflow/api/routes
mkdir -p src/lexiflow/api/schemas
mkdir -p src/lexiflow/core/interfaces
mkdir -p src/lexiflow/infrastructure/vector_stores
mkdir -p src/lexiflow/infrastructure/embedders
mkdir -p src/lexiflow/infrastructure/llm
mkdir -p src/lexiflow/infrastructure/parsers
mkdir -p src/lexiflow/agents
mkdir -p src/lexiflow/orchestration
mkdir -p src/lexiflow/services
mkdir -p tests/unit
mkdir -p tests/integration

# Create __init__.py files to make Python packages
touch src/__init__.py
touch src/lexiflow/__init__.py
touch src/lexiflow/api/__init__.py
touch src/lexiflow/api/routes/__init__.py
touch src/lexiflow/api/schemas/__init__.py
touch src/lexiflow/core/__init__.py
touch src/lexiflow/core/interfaces/__init__.py
touch src/lexiflow/infrastructure/__init__.py
touch src/lexiflow/infrastructure/vector_stores/__init__.py
touch src/lexiflow/infrastructure/embedders/__init__.py
touch src/lexiflow/infrastructure/llm/__init__.py
touch src/lexiflow/infrastructure/parsers/__init__.py
touch src/lexiflow/agents/__init__.py
touch src/lexiflow/orchestration/__init__.py
touch src/lexiflow/services/__init__.py