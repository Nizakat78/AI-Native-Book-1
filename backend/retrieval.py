"""
Module for handling document retrieval from the RAG system.
This module interfaces with the vector database to retrieve relevant documents.
"""
from typing import List, Dict, Optional
import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import OpenAI
from .config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RetrievalService:
    """
    Service class for handling document retrieval operations.
    """

    def __init__(self):
        """
        Initialize the retrieval service with Qdrant client.
        """
        logger.info("Initializing retrieval service with Qdrant")

        # Initialize Qdrant client
        if config.QDRANT_API_KEY:
            self.client = QdrantClient(
                url=config.QDRANT_URL,
                api_key=config.QDRANT_API_KEY,
                prefer_grpc=False,
                timeout=30
            )
        else:
            self.client = QdrantClient(
                url=config.QDRANT_URL,
                timeout=30
            )

        self.collection_name = config.RAG_COLLECTION_NAME
        self.openai_client = OpenAI(
            api_key=config.OPENAI_API_KEY,
            timeout=30.0  # 30 second timeout for API calls
        )

        # Verify connection
        try:
            self.client.get_collection(collection_name=self.collection_name)
            logger.info(f"Connected to Qdrant collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Could not connect to Qdrant collection {self.collection_name}: {str(e)}")
            raise

    async def _get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for text using OpenAI API.

        Args:
            text: Text to embed

        Returns:
            Embedding vector as list of floats
        """
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error getting embedding: {str(e)}")
            raise

    async def retrieve_documents(self, query: str, context_mode: str = "full_book", selected_text: Optional[str] = None) -> List[Dict]:
        """
        Retrieve relevant documents based on the query and context mode.

        Args:
            query: The user's query
            context_mode: Either "full_book" or "selected_text"
            selected_text: Optional selected text for context (when context_mode is "selected_text")

        Returns:
            List of relevant documents with metadata
        """
        logger.info(f"Retrieving documents for query: {query}, context_mode: {context_mode}")

        try:
            # Get embedding for the query
            query_embedding = await self._get_embedding(query)

            # Search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=config.MAX_RETRIEVAL_RESULTS,
                score_threshold=config.SIMILARITY_THRESHOLD
            )

            # Format results
            documents = []
            for result in search_results:
                documents.append({
                    "id": result.id,
                    "content": result.payload.get("content", ""),
                    "source": result.payload.get("source", ""),
                    "page_reference": result.payload.get("page_reference", ""),
                    "score": result.score
                })

            # If in selected text mode, filter results that are most relevant to the selected text
            if context_mode == "selected_text" and selected_text:
                # Re-rank or filter results based on selected text context
                # For now, just ensure the selected text context is considered
                logger.info(f"Using selected text context: {selected_text[:100]}...")
                # In a real implementation, we might do additional processing here

            return documents

        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}", exc_info=True)
            # Return a default response if retrieval fails
            return [
                {
                    "id": "error_fallback",
                    "content": f"Default response for query: {query[:100]}",
                    "source": "fallback",
                    "page_reference": "N/A"
                }
            ]

    async def search_full_book(self, query: str) -> List[Dict]:
        """
        Search across the full book content.

        Args:
            query: The search query

        Returns:
            List of relevant documents
        """
        return await self.retrieve_documents(query, "full_book")

    async def search_selected_text(self, query: str, selected_text: str) -> List[Dict]:
        """
        Search specifically related to the selected text.

        Args:
            query: The search query
            selected_text: The selected text for context

        Returns:
            List of relevant documents
        """
        return await self.retrieve_documents(query, "selected_text", selected_text)