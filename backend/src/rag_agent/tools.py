"""
Tools module for RAG Agent with OpenAI Agents SDK.

This module contains function tools that can be used by the OpenAI agent.
"""
import os
from typing import List, Dict, Any
from agents import function_tool
from qdrant_client import QdrantClient
from cohere import Client as CohereClient
import logging

logger = logging.getLogger(__name__)

# Initialize clients globally to avoid repeated initialization
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
cohere_api_key = os.getenv("COHERE_API_KEY")
collection_name = os.getenv("QDRANT_COLLECTION", "rag_embeddings")

if not qdrant_url:
    raise ValueError("QDRANT_URL environment variable is required")
if not qdrant_api_key:
    raise ValueError("QDRANT_API_KEY environment variable is required")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY environment variable is required")

qdrant_client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key,
    timeout=10
)

cohere_client = CohereClient(api_key=cohere_api_key)


def _internal_retrieve_content(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Internal function to retrieve relevant content from the AI textbook based on semantic similarity.

    Args:
        query: The search query to find relevant content
        top_k: Number of results to return (default: 5)

    Returns:
        List of content results with metadata
    """
    try:
        # Embed the query text using Cohere to get a vector representation
        query_embeddings = cohere_client.embed(
            texts=[query],
            model="embed-english-v3.0",
            input_type="search_query"
        )
        query_vector = query_embeddings.embeddings[0]

        # Perform vector search in Qdrant
        search_results = qdrant_client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=top_k,
            with_payload=True,
            with_vectors=False
        )

        # query_points returns a QueryResponse object with 'points' attribute
        search_points = search_results.points if hasattr(search_results, 'points') else search_results

        # Convert Qdrant results to a simple dictionary format for the agent
        results = []
        for result in search_points:
            # Extract metadata from the Qdrant result
            payload = result.payload or {}

            result_dict = {
                "content": payload.get('content', ''),
                "url": payload.get('url', ''),
                "section": payload.get('section', ''),
                "chunk_index": payload.get('chunk_index', -1),
                "score": result.score,
                "metadata": payload
            }
            results.append(result_dict)

        # Results from Qdrant search are already sorted by score in descending order
        logger.info(f"Retrieval completed for query: '{query[:50]}...', found {len(results)} results")
        return results

    except Exception as e:
        logger.error(f"Retrieval failed for query '{query}': {str(e)}")
        # Handle specific edge cases
        error_msg = str(e)
        if "rate limit" in error_msg.lower() or "429" in error_msg:
            logger.error("Rate limit exceeded - consider implementing rate limiting")
            # Return empty results instead of raising exception for rate limiting
            return []
        elif "connection" in error_msg.lower() or "timeout" in error_msg.lower():
            logger.error("Connection timeout - consider retry logic")
            return []
        else:
            # For other errors, return empty list
            return []


@function_tool
def retrieve_content(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve relevant content from the AI textbook based on semantic similarity.

    Args:
        query: The search query to find relevant content
        top_k: Number of results to return (default: 5)

    Returns:
        List of content results with metadata
    """
    # Call the internal function
    return _internal_retrieve_content(query, top_k)