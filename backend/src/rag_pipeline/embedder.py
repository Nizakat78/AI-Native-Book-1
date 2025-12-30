"""Embedder module for generating vector embeddings using Cohere."""

import cohere
from typing import List, Dict, Any
import logging
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class Embedder:
    """Cohere-based embedder for generating vector embeddings."""

    def __init__(self, api_key: str, model_name: str = "embed-english-v3.0", max_retries: int = 3):
        """
        Initialize the embedder.

        Args:
            api_key: Cohere API key
            model_name: Name of the Cohere embedding model to use
            max_retries: Maximum number of retries for API calls
        """
        self.client = cohere.Client(api_key)
        self.model_name = model_name
        self.max_retries = max_retries

    def embed_texts(self, texts: List[str], input_type: str = "search_document") -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings to embed
            input_type: Type of input for the model (affects how embeddings are generated)

        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.embed(
                    texts=texts,
                    model=self.model_name,
                    input_type=input_type
                )
                return [embedding for embedding in response.embeddings]
            except Exception as e:
                if attempt == self.max_retries:
                    logger.error(f"Failed to generate embeddings after {self.max_retries} retries: {e}")
                    raise
                else:
                    logger.warning(f"Attempt {attempt + 1} failed to generate embeddings: {e}. Retrying...")
                    time.sleep(2 ** attempt)  # Exponential backoff

    def embed_single_text(self, text: str, input_type: str = "search_document") -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text string to embed
            input_type: Type of input for the model

        Returns:
            Embedding vector (list of floats)
        """
        embeddings = self.embed_texts([text], input_type)
        return embeddings[0] if embeddings else []

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the embedding model.

        Returns:
            Dictionary with model information
        """
        # Note: Cohere API doesn't have a direct way to get model info
        # We'll return basic information based on the model name
        return {
            "model_name": self.model_name,
            "description": f"Cohere embedding model: {self.model_name}",
            "input_type": "text",
            "output_type": "vector"
        }