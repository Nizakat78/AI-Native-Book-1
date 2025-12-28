# Data Model: RAG Retrieval Validation

## Entities

### RetrievalResult
**Description**: Represents a single result from the semantic similarity search
**Fields**:
- content: string - The text content of the retrieved chunk
- url: string - Source URL of the content
- section: string - Section identifier within the document
- chunk_index: integer - Index position of the chunk within the document
- score: float - Relevance score from the similarity search
- metadata: object - Additional metadata from Qdrant

### UserQuery
**Description**: Represents a user's search query for validation
**Fields**:
- text: string - The query text
- expected_results: array - Expected content that should be retrieved
- category: string - Category of the query (e.g., "technical", "conceptual")

### ValidationResult
**Description**: Represents the result of validating a retrieval operation
**Fields**:
- query: UserQuery - The original query
- retrieved_results: array - Results returned by the system
- relevance_score: float - Overall relevance of the results
- metadata_completeness: float - Percentage of metadata fields present
- validation_passed: boolean - Whether the validation passed
- errors: array - Any errors encountered during validation

### ConnectionConfig
**Description**: Configuration for connecting to Qdrant Cloud
**Fields**:
- qdrant_url: string - URL of the Qdrant Cloud instance
- qdrant_api_key: string - API key for authentication
- collection_name: string - Name of the vector collection to search
- timeout: integer - Connection timeout in seconds

## Relationships
- UserQuery generates 0..* RetrievalResult through semantic search
- ValidationResult contains 1..* RetrievalResult
- ConnectionConfig used by all retrieval operations

## Validation Rules
- RetrievalResult.url must be a valid URL format
- RetrievalResult.score must be between 0.0 and 1.0
- RetrievalResult.chunk_index must be non-negative
- ValidationResult.metadata_completeness must be between 0.0 and 1.0
- ConnectionConfig.qdrant_url must be a valid HTTPS URL