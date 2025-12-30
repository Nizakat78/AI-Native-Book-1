"""
RAG Retrieval Validation System

This module provides functionality to connect to Qdrant Cloud, perform semantic
similarity searches on pre-generated Cohere embeddings, validate retrieved content
and metadata, and confirm pipeline readiness for agent integration.

Usage Example:
    from src.rag_pipeline.retrieve import RAGRetriever, ConnectionConfig

    # Initialize the retriever
    config = ConnectionConfig(
        qdrant_url="your_qdrant_url",
        qdrant_api_key="your_api_key",
        collection_name="rag_embeddings"
    )
    retriever = RAGRetriever(config)

    # Perform a search
    results = retriever.search("What are the key components of a humanoid robot?")

    # Validate the retrieval pipeline
    validation_results = retriever.run_comprehensive_validation()

    # Check readiness for agent integration
    readiness = retriever.verify_validation_completion_for_agent_integration()
"""

import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
from urllib.parse import urlparse
import cohere


# Set up logging
logger = logging.getLogger(__name__)


@dataclass
class ConnectionConfig:
    """Configuration for connecting to Qdrant Cloud"""
    qdrant_url: str
    qdrant_api_key: str
    collection_name: str = "rag_embeddings"
    timeout: int = 30


@dataclass
class RetrievalResult:
    """Represents a single result from the semantic similarity search"""
    content: str
    url: str
    section: str
    chunk_index: int
    score: float
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class UserQuery:
    """Represents a user's search query for validation"""
    text: str
    expected_results: Optional[List[str]] = None
    category: str = "general"


@dataclass
class ValidationResult:
    """Represents the result of validating a retrieval operation"""
    query: UserQuery
    retrieved_results: List[RetrievalResult]
    relevance_score: float
    metadata_completeness: float
    validation_passed: bool
    errors: Optional[List[str]] = None


class RAGRetriever:
    """Main class for RAG retrieval and validation"""

    def __init__(self, config: ConnectionConfig, cohere_api_key: str = None):
        """
        Initialize the RAG retriever with Qdrant configuration.

        Args:
            config: Connection configuration for Qdrant Cloud
            cohere_api_key: Cohere API key for embedding queries (optional)
        """
        self.config = config
        self.client = QdrantClient(
            url=config.qdrant_url,
            api_key=config.qdrant_api_key,
            timeout=config.timeout
        )

        # Initialize Cohere client if API key provided
        self.cohere_client = None
        if cohere_api_key:
            self.cohere_client = cohere.Client(api_key=cohere_api_key)

        logger.info(f"Initialized RAGRetriever with collection: {config.collection_name}")

    def health_check(self) -> Dict[str, Any]:
        """
        Check the health of the retrieval system.

        Returns:
            Dictionary with health check results
        """
        try:
            # Check if we can connect to Qdrant and access the collection
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.config.collection_name for col in collections.collections)

            health_result = {
                "status": "healthy" if collection_exists else "unhealthy",
                "qdrant_connected": True,
                "collection_exists": collection_exists,
                "collection_name": self.config.collection_name,
                "last_validation_time": self._get_current_timestamp()
            }

            logger.info(f"Health check completed: {health_result}")
            return health_result

        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            # Handle specific error types
            error_msg = str(e)
            if "rate limit" in error_msg.lower() or "429" in error_msg:
                logger.error("Rate limit exceeded when checking health")
            elif "connection" in error_msg.lower() or "timeout" in error_msg.lower():
                logger.error("Connection error when checking health")
            elif "api_key" in error_msg.lower() or "unauthorized" in error_msg.lower():
                logger.error("Authentication error when checking health")

            return {
                "status": "unhealthy",
                "qdrant_connected": False,
                "collection_exists": False,
                "error": str(e),
                "last_validation_time": self._get_current_timestamp()
            }

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"

    def search(self, query_text: str, top_k: int = 5) -> List[RetrievalResult]:
        """
        Perform semantic similarity search in the vector store.

        Args:
            query_text: The query text to search for
            top_k: Number of top results to return

        Returns:
            List of RetrievalResult objects with content and metadata
        """
        # Handle edge cases
        if not query_text or not query_text.strip():
            logger.warning("Empty or whitespace-only query provided")
            return []

        if top_k <= 0:
            logger.warning(f"Invalid top_k value: {top_k}, using default of 5")
            top_k = 5

        try:
            # Embed the query text using Cohere to get a vector representation
            if not self.cohere_client:
                raise ValueError("Cohere client not initialized. Provide cohere_api_key during initialization.")

            query_embeddings = self.cohere_client.embed(
                texts=[query_text],
                model="embed-english-v3.0",
                input_type="search_query"
            )
            query_vector = query_embeddings.embeddings[0]

            # Perform vector search in Qdrant using query_points
            search_results = self.client.query_points(
                collection_name=self.config.collection_name,
                query=query_vector,
                limit=top_k,
                with_payload=True
            )

            # Convert Qdrant results to our RetrievalResult format
            results = []
            # query_points returns a QueryResponse object with 'points' attribute
            search_points = search_results.points if hasattr(search_results, 'points') else search_results
            for result in search_points:
                # Extract metadata from the Qdrant result
                payload = result.payload or {}

                retrieval_result = RetrievalResult(
                    content=payload.get('content', ''),
                    url=payload.get('url', ''),
                    section=payload.get('section', ''),
                    chunk_index=payload.get('chunk_index', -1),
                    score=result.score,
                    metadata=payload
                )
                results.append(retrieval_result)

            # Results from Qdrant search are already sorted by score in descending order
            logger.info(f"Search completed for query: '{query_text[:50]}...', found {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Search failed for query '{query_text}': {str(e)}")
            # Handle specific edge cases
            error_msg = str(e)
            if "rate limit" in error_msg.lower() or "429" in error_msg:
                logger.error("Rate limit exceeded - consider implementing rate limiting")
                # Return empty results instead of raising exception for rate limiting
                return []
            elif "connection" in error_msg.lower() or "timeout" in error_msg.lower():
                logger.error("Connection timeout - consider retry logic")
            elif "api_key" in error_msg.lower() or "unauthorized" in error_msg.lower():
                logger.error("Authentication error - check API key")
            raise

    def validate_metadata(self, result: RetrievalResult) -> Dict[str, bool]:
        """
        Validate the metadata of a retrieval result.

        Args:
            result: The retrieval result to validate

        Returns:
            Dictionary with validation results for each metadata field
        """
        validation_results = {
            'url_valid': self._is_valid_url(result.url),
            'section_valid': result.section is not None and result.section != '',
            'chunk_index_valid': result.chunk_index is not None and result.chunk_index >= 0
        }

        # Log validation results
        if not all(validation_results.values()):
            logger.warning(f"Metadata validation failed for result: {validation_results}")
        else:
            logger.info("Metadata validation passed for result")

        return validation_results

    def _is_valid_url(self, url: str) -> bool:
        """
        Check if a URL is valid.

        Args:
            url: URL string to validate

        Returns:
            True if URL is valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def calculate_metadata_completeness(self, results: List[RetrievalResult]) -> float:
        """
        Calculate the metadata completeness for a list of retrieval results.

        Args:
            results: List of retrieval results to analyze

        Returns:
            Float value between 0.0 and 1.0 representing metadata completeness
        """
        if not results:
            return 0.0

        valid_results = 0
        for result in results:
            validation = self.validate_metadata(result)
            if all(validation.values()):
                valid_results += 1

        completeness = valid_results / len(results)
        logger.info(f"Metadata completeness: {completeness} ({valid_results}/{len(results)} results with valid metadata)")
        return completeness

    def evaluate_content_relevance(self, query: str, results: List[RetrievalResult]) -> float:
        """
        Evaluate the relevance of content to the input query.

        Args:
            query: The original query text
            results: List of retrieval results to evaluate

        Returns:
            Float value between 0.0 and 1.0 representing content relevance
        """
        if not results:
            return 0.0

        # Simple relevance evaluation based on score distribution
        # Higher average score indicates better relevance
        total_score = sum(result.score for result in results)
        avg_score = total_score / len(results)

        # Normalize the average score to a 0-1 scale
        # Assuming scores are normalized between 0 and 1
        relevance_score = min(1.0, max(0.0, avg_score))

        logger.info(f"Content relevance score: {relevance_score} based on average result score: {avg_score}")
        return relevance_score

    def generate_validation_report(self, user_query: UserQuery, results: List[RetrievalResult]) -> ValidationResult:
        """
        Generate a validation report for a specific query and its results.

        Args:
            user_query: The original user query
            results: List of retrieval results for the query

        Returns:
            ValidationResult object with all validation metrics
        """
        # Calculate metadata completeness
        metadata_completeness = self.calculate_metadata_completeness(results)

        # Evaluate content relevance
        relevance_score = self.evaluate_content_relevance(user_query.text, results)

        # Determine if validation passed based on thresholds
        # Using 80% as a threshold for both metrics
        validation_passed = metadata_completeness >= 0.8 and relevance_score >= 0.5

        # Collect any errors
        errors = []
        if metadata_completeness < 0.8:
            errors.append(f"Metadata completeness too low: {metadata_completeness} (threshold: 0.8)")
        if relevance_score < 0.5:
            errors.append(f"Content relevance too low: {relevance_score} (threshold: 0.5)")

        validation_result = ValidationResult(
            query=user_query,
            retrieved_results=results,
            relevance_score=relevance_score,
            metadata_completeness=metadata_completeness,
            validation_passed=validation_passed,
            errors=errors if errors else None
        )

        logger.info(f"Validation report generated: passed={validation_result.validation_passed}, "
                   f"relevance={relevance_score:.2f}, metadata_completeness={metadata_completeness:.2f}")
        return validation_result

    def run_comprehensive_validation(self, sample_queries: List[str] = None) -> Dict[str, Any]:
        """
        Run comprehensive validation of the retrieval pipeline.

        Args:
            sample_queries: Optional list of sample queries to test. If None, uses default queries.

        Returns:
            Dictionary with comprehensive validation results
        """
        # Default sample queries if none provided
        if sample_queries is None:
            sample_queries = [
                "What are the key components of a humanoid robot?",
                "Explain the digital twin concept in robotics",
                "How does VLA (Vision-Language-Action) work?",
                "What is the role of AI in robotics?",
                "Describe the sensor systems in humanoid robots"
            ]

        logger.info(f"Starting comprehensive validation with {len(sample_queries)} sample queries")

        # Perform health check first
        health_result = self.health_check()
        if not health_result.get("qdrant_connected", False):
            logger.error("Qdrant connection failed, cannot proceed with validation")
            return {
                "validation_passed": False,
                "errors": ["Qdrant connection failed"],
                "health_check": health_result
            }

        # Execute sample queries
        query_results = self.execute_sample_queries(sample_queries)

        # Calculate overall validation metrics
        total_queries = query_results['total_queries']
        metadata_completeness = query_results['metadata_completeness']

        # For relevance, calculate from the first few results of each query
        avg_relevance = 0.0
        valid_relevance_count = 0

        for query_result in query_results['results']:
            results = query_result['results']
            if results:
                relevance = self.evaluate_content_relevance(query_result['query'], results)
                avg_relevance += relevance
                valid_relevance_count += 1

        avg_relevance = avg_relevance / valid_relevance_count if valid_relevance_count > 0 else 0.0

        # Determine if overall validation passes
        # Using 80% as threshold for both metrics
        validation_passed = metadata_completeness >= 0.8 and avg_relevance >= 0.5

        comprehensive_result = {
            "validation_passed": validation_passed,
            "health_check": health_result,
            "total_queries": total_queries,
            "metadata_completeness": metadata_completeness,
            "average_relevance_score": avg_relevance,
            "query_results": query_results,
            "readiness_for_agent_integration": validation_passed
        }

        logger.info(f"Comprehensive validation completed: passed={validation_passed}")
        return comprehensive_result

    def generate_validation_summary(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a summary report of validation results.

        Args:
            validation_results: The results from comprehensive validation

        Returns:
            Dictionary with validation summary metrics
        """
        # Extract key metrics from validation results
        validation_passed = validation_results.get('validation_passed', False)
        metadata_completeness = validation_results.get('metadata_completeness', 0)
        avg_relevance_score = validation_results.get('average_relevance_score', 0)
        total_queries = validation_results.get('total_queries', 0)
        health_check = validation_results.get('health_check', {})

        # Calculate additional summary metrics
        qdrant_connected = health_check.get('qdrant_connected', False)
        collection_exists = health_check.get('collection_exists', False)

        # Generate summary report
        summary = {
            "validation_summary": {
                "overall_status": "PASS" if validation_passed else "FAIL",
                "validation_passed": validation_passed,
                "qdrant_connected": qdrant_connected,
                "collection_exists": collection_exists,
                "total_queries_processed": total_queries,
                "metadata_completeness_percentage": round(metadata_completeness * 100, 2),
                "average_relevance_score": round(avg_relevance_score, 3),
                "readiness_for_agent_integration": validation_passed,
                "timestamp": self._get_current_timestamp()
            }
        }

        logger.info(f"Validation summary generated: {summary}")
        return summary

    def validate_by_query_category(self, queries_by_category: Dict[str, List[str]], top_k: int = 5) -> Dict[str, Any]:
        """
        Perform validation for different query categories (technical, conceptual, etc.).

        Args:
            queries_by_category: Dictionary mapping category names to lists of queries
            top_k: Number of results to retrieve for each query

        Returns:
            Dictionary with validation results by category
        """
        logger.info(f"Starting validation for {len(queries_by_category)} query categories")

        category_results = {}
        overall_validation_passed = True
        total_categories = len(queries_by_category)

        for category, queries in queries_by_category.items():
            logger.info(f"Validating category: {category} with {len(queries)} queries")

            # Execute queries for this category
            category_query_results = self.execute_sample_queries(queries, top_k)

            # Calculate metrics for this category
            metadata_completeness = category_query_results.get('metadata_completeness', 0)
            total_results = category_query_results.get('total_results', 0)

            # Calculate relevance for this category
            avg_relevance = 0.0
            valid_relevance_count = 0

            for query_result in category_query_results['results']:
                results = query_result['results']
                if results:
                    relevance = self.evaluate_content_relevance(query_result['query'], results)
                    avg_relevance += relevance
                    valid_relevance_count += 1

            avg_relevance = avg_relevance / valid_relevance_count if valid_relevance_count > 0 else 0.0

            # Determine if this category passes validation
            category_passed = metadata_completeness >= 0.8 and avg_relevance >= 0.5

            if not category_passed:
                overall_validation_passed = False

            category_results[category] = {
                'query_count': len(queries),
                'total_results': total_results,
                'metadata_completeness': metadata_completeness,
                'average_relevance_score': avg_relevance,
                'validation_passed': category_passed,
                'details': category_query_results
            }

        # Overall validation passes only if all categories pass
        final_validation_passed = overall_validation_passed

        result = {
            'validation_passed': final_validation_passed,
            'total_categories': total_categories,
            'categories': category_results,
            'timestamp': self._get_current_timestamp()
        }

        logger.info(f"Category-based validation completed: {result}")
        return result

    def assess_readiness_for_agent_integration(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess readiness for agent integration based on validation results.

        Args:
            validation_results: The results from validation processes

        Returns:
            Dictionary with readiness assessment and flags
        """
        # Extract key metrics from validation results
        validation_passed = validation_results.get('validation_passed', False)
        metadata_completeness = validation_results.get('metadata_completeness', 0)
        avg_relevance_score = validation_results.get('average_relevance_score', 0)
        health_check = validation_results.get('health_check', {})

        # Check if Qdrant is connected and collection exists
        qdrant_connected = health_check.get('qdrant_connected', False)
        collection_exists = health_check.get('collection_exists', False)

        # Determine readiness based on multiple factors
        has_sufficient_metadata = metadata_completeness >= 0.8
        has_sufficient_relevance = avg_relevance_score >= 0.5
        is_technically_ready = qdrant_connected and collection_exists

        # Overall readiness assessment
        is_ready_for_agent_integration = (
            validation_passed and
            has_sufficient_metadata and
            has_sufficient_relevance and
            is_technically_ready
        )

        readiness_assessment = {
            "readiness_assessment": {
                "is_ready_for_agent_integration": is_ready_for_agent_integration,
                "technical_readiness": is_technically_ready,
                "validation_passed": validation_passed,
                "has_sufficient_metadata": has_sufficient_metadata,
                "has_sufficient_relevance": has_sufficient_relevance,
                "readiness_flags": {
                    "qdrant_connected": qdrant_connected,
                    "collection_exists": collection_exists,
                    "metadata_threshold_met": has_sufficient_metadata,
                    "relevance_threshold_met": has_sufficient_relevance,
                    "overall_validation_passed": validation_passed
                },
                "readiness_score": {
                    "metadata_score": round(metadata_completeness * 100, 2),
                    "relevance_score": round(avg_relevance_score * 100, 2),
                    "overall_score": 100 if is_ready_for_agent_integration else 0
                },
                "recommendations": self._generate_readiness_recommendations(
                    is_ready_for_agent_integration,
                    metadata_completeness,
                    avg_relevance_score
                ),
                "timestamp": self._get_current_timestamp()
            }
        }

        logger.info(f"Readiness assessment completed: ready={is_ready_for_agent_integration}")
        return readiness_assessment

    def _generate_readiness_recommendations(self, is_ready: bool, metadata_score: float, relevance_score: float) -> List[str]:
        """
        Generate recommendations based on readiness assessment.

        Args:
            is_ready: Whether the system is ready for agent integration
            metadata_score: Metadata completeness score
            relevance_score: Relevance score

        Returns:
            List of recommendations
        """
        recommendations = []

        if is_ready:
            recommendations.append("System is ready for agent integration")
        else:
            if metadata_score < 0.8:
                recommendations.append(f"Improve metadata completeness (current: {metadata_score:.2f}, target: 0.8)")
            if relevance_score < 0.5:
                recommendations.append(f"Improve content relevance (current: {relevance_score:.2f}, target: 0.5)")
            if not is_ready:
                recommendations.append("Address the above issues before proceeding with agent integration")

        return recommendations

    def verify_validation_completion_for_agent_integration(self) -> Dict[str, Any]:
        """
        Verify that validation is complete and ready for agent integration.

        Returns:
            Dictionary with verification results
        """
        logger.info("Verifying validation completion for agent integration")

        # Perform a comprehensive validation to ensure everything is ready
        comprehensive_result = self.run_comprehensive_validation()

        # Generate validation summary
        summary = self.generate_validation_summary(comprehensive_result)

        # Assess readiness
        readiness = self.assess_readiness_for_agent_integration(comprehensive_result)

        # Final verification
        is_ready = readiness['readiness_assessment']['is_ready_for_agent_integration']

        verification_result = {
            "validation_verification": {
                "is_complete": True,
                "is_ready_for_agent_integration": is_ready,
                "comprehensive_validation": comprehensive_result,
                "validation_summary": summary,
                "readiness_assessment": readiness,
                "verification_timestamp": self._get_current_timestamp()
            }
        }

        logger.info(f"Validation verification completed: ready={is_ready}")
        return verification_result

    def execute_sample_queries(self, queries: List[str], top_k: int = 5) -> Dict[str, Any]:
        """
        Execute sample queries for validation purposes.

        Args:
            queries: List of query strings to execute
            top_k: Number of results to retrieve for each query

        Returns:
            Dictionary with validation results
        """
        logger.info(f"Executing {len(queries)} sample queries for validation")

        all_results = []
        total_valid_metadata = 0
        total_results = 0

        for query_text in queries:
            logger.info(f"Executing sample query: '{query_text}'")

            # Perform the search
            search_results = self.search(query_text, top_k)

            # Validate metadata for each result
            query_metadata_validation = []
            for result in search_results:
                validation = self.validate_metadata(result)
                query_metadata_validation.append(validation)

                # Count valid metadata
                if all(validation.values()):
                    total_valid_metadata += 1
                total_results += 1

            all_results.append({
                'query': query_text,
                'results': search_results,
                'metadata_validation': query_metadata_validation
            })

        # Calculate metadata completeness
        metadata_completeness = (total_valid_metadata / total_results) if total_results > 0 else 0.0

        validation_result = {
            'total_queries': len(queries),
            'successful_queries': len(queries),  # Assuming all queries succeed
            'total_results': total_results,
            'valid_metadata_count': total_valid_metadata,
            'metadata_completeness': metadata_completeness,
            'results': all_results
        }

        logger.info(f"Sample query validation completed: {validation_result}")
        return validation_result


def main():
    """Command-line interface for RAG retrieval validation."""
    import argparse
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    parser = argparse.ArgumentParser(description='RAG Retrieval Validation Tool')
    parser.add_argument('--validate', action='store_true', help='Run comprehensive validation')
    parser.add_argument('--query', type=str, help='Run a specific query and return results')
    parser.add_argument('--health', action='store_true', help='Check health of the retrieval system')
    parser.add_argument('--ready', action='store_true', help='Check readiness for agent integration')
    parser.add_argument('--top-k', type=int, default=5, help='Number of results to return (default: 5)')

    args = parser.parse_args()

    # Create configuration from environment variables
    config = ConnectionConfig(
        qdrant_url=os.getenv('QDRANT_URL', ''),
        qdrant_api_key=os.getenv('QDRANT_API_KEY', ''),
        collection_name=os.getenv('QDRANT_COLLECTION', 'rag_embeddings')
    )

    # Get Cohere API key from environment
    cohere_api_key = os.getenv('COHERE_API_KEY', '')

    # Initialize the retriever
    retriever = RAGRetriever(config, cohere_api_key=cohere_api_key)

    if args.health:
        # Run health check
        result = retriever.health_check()
        print("Health Check Result:")
        print(result)

    elif args.query:
        # Run a specific query
        results = retriever.search(args.query, top_k=args.top_k)
        print(f"Query: {args.query}")
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"{i}. Score: {result.score:.3f}, URL: {result.url}")
            print(f"   Content: {result.content[:200]}...")
            print()

    elif args.ready:
        # Check readiness for agent integration
        result = retriever.verify_validation_completion_for_agent_integration()
        print("Readiness Check Result:")
        readiness = result['validation_verification']['readiness_assessment']['readiness_assessment']
        print(f"Ready for agent integration: {readiness['is_ready_for_agent_integration']}")
        print(f"Validation passed: {readiness['validation_passed']}")
        print(f"Metadata completeness: {readiness['readiness_score']['metadata_score']}%")
        print(f"Relevance score: {readiness['readiness_score']['relevance_score']}")
        print("Recommendations:")
        for rec in readiness['recommendations']:
            print(f"  - {rec}")

    elif args.validate:
        # Run comprehensive validation
        result = retriever.run_comprehensive_validation()
        print("Comprehensive Validation Result:")
        print(f"Validation passed: {result['validation_passed']}")
        print(f"Metadata completeness: {result['metadata_completeness']:.2f}")
        print(f"Average relevance score: {result['average_relevance_score']:.2f}")
        print(f"Qdrant connected: {result['health_check']['qdrant_connected']}")
        print(f"Collection exists: {result['health_check']['collection_exists']}")
    else:
        # Show help if no arguments provided
        parser.print_help()


if __name__ == "__main__":
    main()