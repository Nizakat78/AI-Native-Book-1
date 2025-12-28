"""Configuration management for the RAG pipeline."""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class Config:
    """Configuration class holding all settings for the RAG pipeline."""

    # API Keys and URLs
    cohere_api_key: str
    qdrant_url: str
    qdrant_api_key: str
    base_url: str

    # Processing parameters
    chunk_size: int = 1000
    chunk_overlap: int = 100
    batch_size: int = 10
    max_retries: int = 3
    delay_between_requests: float = 1.0

    @classmethod
    def from_env(cls) -> 'Config':
        """Create a Config instance from environment variables."""
        return cls(
            cohere_api_key=os.getenv('COHERE_API_KEY', ''),
            qdrant_url=os.getenv('QDRANT_URL', ''),
            qdrant_api_key=os.getenv('QDRANT_API_KEY', ''),
            base_url=os.getenv('BASE_URL', ''),
            chunk_size=int(os.getenv('CHUNK_SIZE', '1000')),
            chunk_overlap=int(os.getenv('CHUNK_OVERLAP', '100')),
            batch_size=int(os.getenv('BATCH_SIZE', '10')),
            max_retries=int(os.getenv('MAX_RETRIES', '3')),
            delay_between_requests=float(os.getenv('DELAY_BETWEEN_REQUESTS', '1.0'))
        )

    def validate(self) -> bool:
        """Validate that required configuration values are present."""
        required_fields = [
            self.cohere_api_key,
            self.qdrant_url,
            self.qdrant_api_key,
            self.base_url
        ]

        return all(field.strip() for field in required_fields)