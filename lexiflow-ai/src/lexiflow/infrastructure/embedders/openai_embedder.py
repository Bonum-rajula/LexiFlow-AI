# src/lexiflow/infrastructure/embedders/openai_embedder.py
from typing import List
from openai import OpenAI

from ...core.interfaces import Embedder
from ...core.config import settings


class OpenAIEmbedder(Embedder):
    """Concrete embedder using OpenAI's text-embedding-3-small model."""

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.embedding_model

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string."""
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
            encoding_format="float",
        )
        return response.data[0].embedding

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a batch of document chunks."""
        # OpenAI handles batching natively; we can send up to 2048 texts at once.
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
            encoding_format="float",
        )
        # Ensure embeddings are returned in the same order as input.
        embeddings = [data.embedding for data in response.data]
        return embeddings

    @property
    def embedding_dimension(self) -> int:
        """Return the dimension for text-embedding-3-small (1536)."""
        return 1536