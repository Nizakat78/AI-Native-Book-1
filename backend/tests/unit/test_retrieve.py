"""
Unit tests for the RAG retrieval validation system.
"""
import unittest
from unittest.mock import Mock, patch
from src.rag_pipeline.retrieve import RAGRetriever, ConnectionConfig, RetrievalResult


class TestRAGRetriever(unittest.TestCase):
    """Unit tests for the RAGRetriever class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        config = ConnectionConfig(
            qdrant_url="test_url",
            qdrant_api_key="test_key"
        )
        self.retriever = RAGRetriever(config)

    def test_connection_config_initialization(self):
        """Test that ConnectionConfig is properly initialized."""
        config = ConnectionConfig(
            qdrant_url="test_url",
            qdrant_api_key="test_key",
            collection_name="test_collection",
            timeout=60
        )

        self.assertEqual(config.qdrant_url, "test_url")
        self.assertEqual(config.qdrant_api_key, "test_key")
        self.assertEqual(config.collection_name, "test_collection")
        self.assertEqual(config.timeout, 60)

    def test_retrieval_result_creation(self):
        """Test that RetrievalResult is properly created."""
        result = RetrievalResult(
            content="test content",
            url="https://example.com",
            section="test section",
            chunk_index=0,
            score=0.95
        )

        self.assertEqual(result.content, "test content")
        self.assertEqual(result.url, "https://example.com")
        self.assertEqual(result.section, "test section")
        self.assertEqual(result.chunk_index, 0)
        self.assertEqual(result.score, 0.95)

    @patch('src.rag_pipeline.retrieve.QdrantClient')
    def test_health_check(self, mock_qdrant_client):
        """Test the health check functionality."""
        # Mock the Qdrant client and its methods
        mock_client = Mock()
        mock_client.get_collections.return_value = Mock()
        mock_client.get_collections.return_value.collections = [Mock(name="rag_embeddings")]
        self.retriever.client = mock_client

        # Run health check
        result = self.retriever.health_check()

        # Verify the result
        self.assertTrue(result["qdrant_connected"])
        self.assertTrue(result["collection_exists"])
        self.assertEqual(result["status"], "healthy")

    def test_is_valid_url(self):
        """Test URL validation."""
        # Valid URLs
        self.assertTrue(self.retriever._is_valid_url("https://example.com"))
        self.assertTrue(self.retriever._is_valid_url("http://example.com/path"))

        # Invalid URLs
        self.assertFalse(self.retriever._is_valid_url("invalid_url"))
        self.assertFalse(self.retriever._is_valid_url(""))
        self.assertFalse(self.retriever._is_valid_url("ftp://example.com"))  # Only http/https allowed


if __name__ == '__main__':
    unittest.main()