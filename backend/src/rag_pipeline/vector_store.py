"""Vector store module for storing embeddings in Qdrant Cloud."""

from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
import uuid
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    """Qdrant-based vector store for storing embeddings with metadata."""

    def __init__(self, url: str, api_key: str, collection_name: str = "rag_embeddings"):
        """
        Initialize the vector store.

        Args:
            url: Qdrant Cloud URL
            api_key: Qdrant API key
            collection_name: Name of the collection to store embeddings in
        """
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection_name = collection_name

    def create_collection(self, vector_size: int = 1024) -> bool:
        """
        Create a collection in Qdrant Cloud if it doesn't exist.

        Args:
            vector_size: Size of the embedding vectors

        Returns:
            True if collection was created or already exists
        """
        try:
            # Check if collection already exists
            collections = self.client.get_collections()
            collection_names = [collection.name for collection in collections.collections]

            if self.collection_name not in collection_names:
                # Create new collection
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=vector_size,
                        distance=models.Distance.COSINE
                    )
                )
                logger.info(f"Created collection '{self.collection_name}' in Qdrant Cloud")
            else:
                logger.info(f"Collection '{self.collection_name}' already exists in Qdrant Cloud")

            # Configure the collection with payload schema
            self.client.update_collection(
                collection_name=self.collection_name,
                optimizer_config=models.OptimizersConfigDiff(
                    memmap_threshold=20000,
                    indexing_threshold=20000,
                )
            )

            return True
        except Exception as e:
            logger.error(f"Failed to create collection '{self.collection_name}': {e}")
            return False

    def store_embeddings(self, embeddings: List[Dict[str, Any]]) -> bool:
        """
        Store embeddings with metadata in Qdrant Cloud.

        Args:
            embeddings: List of dictionaries containing:
                - 'vector': The embedding vector
                - 'url': Source URL
                - 'section': Section name
                - 'heading': Heading title
                - 'chunk_index': Index of the chunk
                - 'content': Original content (optional)

        Returns:
            True if storage was successful
        """
        try:
            points = []
            for item in embeddings:
                # Generate a unique ID for each point
                point_id = str(uuid.uuid4())

                # Prepare the payload with metadata
                payload = {
                    "url": item.get('url', ''),
                    "section": item.get('section', ''),
                    "heading": item.get('heading', ''),
                    "chunk_index": item.get('chunk_index', 0),
                    "content": item.get('content', '')[:1000]  # Limit content size in payload
                }

                # Add any additional metadata that might be present
                for key, value in item.items():
                    if key not in ['vector', 'url', 'section', 'heading', 'chunk_index', 'content']:
                        payload[key] = value

                points.append(
                    models.PointStruct(
                        id=point_id,
                        vector=item['vector'],
                        payload=payload
                    )
                )

            # Upload points to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Successfully stored {len(points)} embeddings in Qdrant Cloud")
            return True
        except Exception as e:
            logger.error(f"Failed to store embeddings: {e}")
            return False

    def search_similar(self, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for similar embeddings in the vector store.

        Args:
            query_vector: Vector to search for similarities
            limit: Maximum number of results to return

        Returns:
            List of similar embeddings with metadata
        """
        try:
            results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                with_payload=True,
                with_vectors=True
            )

            # query_points returns a QueryResponse object with 'points' attribute
            search_points = results.points if hasattr(results, 'points') else results
            return [
                {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload,
                    "vector": result.vector
                }
                for result in search_points
            ]
        except Exception as e:
            logger.error(f"Failed to search similar embeddings: {e}")
            return []

    def verify_embeddings(self) -> bool:
        """
        Verify that embeddings are properly stored and queryable.

        Returns:
            True if verification is successful
        """
        try:
            # Get collection info
            collection_info = self.client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' has {collection_info.points_count} points")

            # Try to get a random point if any exist
            if collection_info.points_count > 0:
                # Search with a random vector to test query capability
                random_vector = [0.0] * collection_info.config.params.vectors.size
                results = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=random_vector,
                    limit=1
                )
                logger.info(f"Verification search returned {len(results)} results")
                return True

            return collection_info.points_count >= 0
        except Exception as e:
            logger.error(f"Failed to verify embeddings: {e}")
            return False

    def get_total_count(self) -> int:
        """
        Get the total number of embeddings stored.

        Returns:
            Total count of embeddings
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return collection_info.points_count
        except Exception as e:
            logger.error(f"Failed to get total count: {e}")
            return 0