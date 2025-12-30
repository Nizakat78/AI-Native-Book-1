"""
Configuration module for the RAG chatbot system.
This module handles environment variables and configuration settings.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class to manage environment settings.
    """

    # API Configuration
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: Optional[str] = os.getenv("QDRANT_API_KEY")

    # Application settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # RAG settings
    RAG_COLLECTION_NAME: str = os.getenv("RAG_COLLECTION_NAME", "book_content")
    MAX_RETRIEVAL_RESULTS: int = int(os.getenv("MAX_RETRIEVAL_RESULTS", "5"))
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))

    # Frontend settings
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # Validation
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that required configuration values are set.

        Returns:
            True if configuration is valid, False otherwise
        """
        if not cls.OPENROUTER_API_KEY:
            print("Warning: OPENROUTER_API_KEY is not set in environment")
            return False

        return True

# Initialize configuration
config = Config()

# Validate configuration on import
if not config.validate():
    print("Configuration validation failed - some settings may be missing")