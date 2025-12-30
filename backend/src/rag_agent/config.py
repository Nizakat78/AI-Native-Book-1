"""
Configuration module for RAG Agent with OpenAI Agents SDK.

This module handles application configuration and settings.
"""
import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class Config:
    """
    Application configuration class that holds all settings.
    """
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENROUTER_API_KEY", "")

    # Qdrant Configuration
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "rag_embeddings")

    # Cohere Configuration
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")

    # FastAPI Configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Agent Configuration
    agent_model: str = os.getenv("AGENT_MODEL", "gpt-4-turbo")
    retrieval_top_k: int = int(os.getenv("RETRIEVAL_TOP_K", "5"))

    def __post_init__(self):
        """
        Validate required configuration after initialization.
        """
        if not self.openai_api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        if not self.qdrant_url:
            raise ValueError("QDRANT_URL environment variable is required")
        if not self.qdrant_api_key:
            raise ValueError("QDRANT_API_KEY environment variable is required")
        if not self.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")


# Global configuration instance
config = Config()


def get_config() -> Config:
    """
    Get the application configuration.

    Returns:
        Config: The application configuration instance
    """
    return config