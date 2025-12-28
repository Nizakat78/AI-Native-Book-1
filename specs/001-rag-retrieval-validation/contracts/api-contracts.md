# API Contracts: RAG Retrieval Validation

## Overview
This document defines the API contracts for the RAG retrieval validation system. Since this is primarily a validation tool, the contracts focus on the internal API that will be used for validation operations.

## Endpoints

### POST /validate-retrieval
**Description**: Validates the RAG retrieval pipeline with sample queries

**Request**:
```json
{
  "sample_queries": [
    {
      "text": "What are the key components of a humanoid robot?",
      "expected_content": ["actuators", "sensors", "control systems"]
    }
  ],
  "collection_name": "rag_embeddings"
}
```

**Response**:
```json
{
  "validation_passed": true,
  "total_queries": 1,
  "successful_queries": 1,
  "metadata_completeness": 1.0,
  "average_relevance_score": 0.85,
  "results": [
    {
      "query": "What are the key components of a humanoid robot?",
      "retrieved_results": [
        {
          "content": "Humanoid robots consist of multiple components...",
          "url": "https://ai-native-book-1.vercel.app/docs/humanoid-robotics-modules/intro",
          "section": "Introduction",
          "chunk_index": 0,
          "score": 0.92
        }
      ],
      "relevance_score": 0.92,
      "metadata_completeness": 1.0,
      "validation_passed": true
    }
  ]
}
```

### POST /search
**Description**: Performs semantic similarity search in the vector store

**Request**:
```json
{
  "query": "What are the key components of a humanoid robot?",
  "top_k": 5,
  "collection_name": "rag_embeddings"
}
```

**Response**:
```json
{
  "results": [
    {
      "content": "Humanoid robots consist of multiple components...",
      "url": "https://ai-native-book-1.vercel.app/docs/humanoid-robotics-modules/intro",
      "section": "Introduction",
      "chunk_index": 0,
      "score": 0.92
    }
  ]
}
```

### GET /health
**Description**: Checks the health of the retrieval system

**Response**:
```json
{
  "status": "healthy",
  "qdrant_connected": true,
  "collection_exists": true,
  "last_validation_time": "2025-12-26T10:00:00Z"
}
```

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "error": {
    "code": "CONNECTION_ERROR",
    "message": "Failed to connect to Qdrant Cloud",
    "details": "Check QDRANT_URL and QDRANT_API_KEY configuration"
  }
}
```

## Common Error Codes
- `CONNECTION_ERROR`: Unable to connect to Qdrant Cloud
- `COLLECTION_NOT_FOUND`: Specified collection does not exist
- `VALIDATION_FAILED`: Validation did not meet required thresholds
- `QUERY_TOO_SHORT`: Query text is too short for meaningful search
- `RATE_LIMIT_EXCEEDED`: Qdrant Cloud rate limits exceeded