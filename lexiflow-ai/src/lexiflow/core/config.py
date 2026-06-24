# src/lexiflow/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # LLM
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4o-mini", alias="OPENAI_MODEL")
    embedding_model: str = Field("text-embedding-3-small", alias="EMBEDDING_MODEL")
    
    # ChromaDB
    chroma_host: str = Field("localhost", alias="CHROMA_HOST")
    chroma_port: int = Field(8000, alias="CHROMA_PORT")
    chroma_collection: str = Field("lexiflow_docs", alias="CHROMA_COLLECTION")
    
    # Application Tuning
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    max_chunk_size: int = Field(512, alias="MAX_CHUNK_SIZE")
    chunk_overlap: int = Field(50, alias="CHUNK_OVERLAP")
    
    # Derived properties for convenience
    @property
    def chroma_http_url(self) -> str:
        return f"http://{self.chroma_host}:{self.chroma_port}"


# Singleton instance to import globally
settings = Settings()