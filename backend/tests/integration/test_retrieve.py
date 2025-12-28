"""
Integration tests for the RAG retrieval validation system.
"""
import unittest
import os
from unittest.mock import patch
from src.rag_pipeline.retrieve import RAGRetriever, ConnectionConfig


class TestRAGRetrieverIntegration(unittest.TestCase):
    """Integration tests for the RAGRetriever class."""

    def setUp(self):
        """Set up test configuration using environment variables."""
        qdrant_url = os.getenv('QDRANT_URL', '')
        qdrant_api_key = os.getenv('QDRANT_API_KEY', '')

        if not qdrant_url or not qdrant_api_key:
            # If environment variables aren't set, skip tests or use mock
            self.skip_test = True
            return

        config = ConnectionConfig(
            qdrant_url=qdrant_url,
            qdrant_api_key=qdrant_api_key
        )
        self.retriever = RAGRetriever(config)
        self.skip_test = False

    @unittest.skipIf(os.getenv('QDRANT_URL') is None or os.getenv('QDRANT_API_KEY') is None,
                     "QDRANT_URL or QDRANT_API_KEY not set in environment")
    def test_health_check_integration(self):
        """Test the health check with real Qdrant connection."""
        if self.skip_test:
            self.skipTest("Environment variables not set for integration test")

        result = self.retriever.health_check()

        # Should be connected to Qdrant
        self.assertTrue(result["qdrant_connected"])
        self.assertIsNotNone(result["collection_name"])
        self.assertIn("last_validation_time", result)

    @unittest.skipIf(os.getenv('QDRANT_URL') is None or os.getenv('QDRANT_API_KEY') is None,
                     "QDRANT_URL or QDRANT_API_KEY not set in environment")
    def test_search_integration(self):
        """Test the search functionality with real Qdrant connection."""
        if self.skip_test:
            self.skipTest("Environment variables not set for integration test")

        # Test with a simple query
        results = self.retriever.search("humanoid robot", top_k=3)

        # Should return a list of results
        self.assertIsInstance(results, list)
        self.assertLessEqual(len(results), 3)  # At most 3 results requested

        # If we got results, check their structure
        if results:
            for result in results:
                self.assertIsNotNone(result.content)
                self.assertIsNotNone(result.url)
                self.assertIsNotNone(result.score)

    @unittest.skipIf(os.getenv('QDRANT_URL') is None or os.getenv('QDRANT_API_KEY') is None,
                     "QDRANT_URL or QDRANT_API_KEY not set in environment")
    def test_comprehensive_validation_integration(self):
        """Test the comprehensive validation pipeline."""
        if self.skip_test:
            self.skipTest("Environment variables not set for integration test")

        # Run a small validation with minimal sample queries
        sample_queries = ["humanoid robot", "AI", "machine learning"]
        result = self.retriever.run_comprehensive_validation(sample_queries)

        # Should have a validation result
        self.assertIn("validation_passed", result)
        self.assertIn("health_check", result)
        self.assertIn("query_results", result)

        # Health check should show connection
        self.assertTrue(result["health_check"]["qdrant_connected"])

    @unittest.skipIf(os.getenv('QDRANT_URL') is None or os.getenv('QDRANT_API_KEY') is None,
                     "QDRANT_URL or QDRANT_API_KEY not set in environment")
    def test_metadata_validation_integration(self):
        """Test metadata validation with real search results."""
        if self.skip_test:
            self.skipTest("Environment variables not set for integration test")

        # Perform a search to get results
        results = self.retriever.search("robotics", top_k=2)

        if results:
            # Test metadata validation on the first result
            first_result = results[0]
            validation = self.retriever.validate_metadata(first_result)

            # Should validate all metadata fields
            self.assertIn("url_valid", validation)
            self.assertIn("section_valid", validation)
            self.assertIn("chunk_index_valid", validation)


if __name__ == '__main__':
    unittest.main()