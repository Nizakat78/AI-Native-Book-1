# Quickstart: RAG Retrieval Validation

## Overview
This guide explains how to set up and run the RAG retrieval validation system to validate your Qdrant Cloud vector store with pre-generated Cohere embeddings.

## Prerequisites
- Python 3.11+
- Qdrant Cloud account and API key
- Access to pre-generated Cohere embeddings in Qdrant Cloud
- Python virtual environment (recommended)

## Setup

1. **Install dependencies**:
   ```bash
   # If using uv (as per existing project)
   cd backend
   uv sync
   ```

2. **Configure environment variables**:
   Create a `.env` file in the backend directory with:
   ```env
   QDRANT_URL=your_qdrant_cloud_url
   QDRANT_API_KEY=your_qdrant_api_key
   COHERE_API_KEY=your_cohere_api_key  # for potential future use
   ```

3. **Verify Qdrant connection**:
   Ensure your Qdrant Cloud instance is accessible and contains the expected collection with embeddings.

## Running Validation

1. **Execute the retrieval validation using command line**:
   ```bash
   cd backend
   python src/rag_pipeline/retrieve.py --validate
   ```

2. **Check system health**:
   ```bash
   cd backend
   python src/rag_pipeline/retrieve.py --health
   ```

3. **Test a specific query**:
   ```bash
   cd backend
   python src/rag_pipeline/retrieve.py --query "What are the key components of a humanoid robot?"
   ```

4. **Check readiness for agent integration**:
   ```bash
   cd backend
   python src/rag_pipeline/retrieve.py --ready
   ```

## Sample Usage

```python
from src.rag_pipeline.retrieve import RAGRetriever, ConnectionConfig

# Initialize the retriever
config = ConnectionConfig(
    qdrant_url="your_qdrant_url",
    qdrant_api_key="your_api_key",
    collection_name="rag_embeddings"
)
retriever = RAGRetriever(config)

# Perform a semantic search
results = retriever.search("What are the key components of a humanoid robot?")

# Run comprehensive validation
validation_results = retriever.run_comprehensive_validation()

# Check readiness for agent integration
readiness = retriever.verify_validation_completion_for_agent_integration()

print(f"Ready for agent integration: {readiness['validation_verification']['is_ready_for_agent_integration']}")
```

## Expected Output

The validation will output:
- Connection status to Qdrant Cloud
- Number of successful queries tested
- Metadata completeness percentage
- Overall relevance scores
- Validation pass/fail status

Example:
```
Comprehensive Validation Result:
Validation passed: True
Metadata completeness: 0.95
Average relevance score: 0.82
Qdrant connected: True
Collection exists: True
```

## Troubleshooting

- **Connection errors**: Verify QDRANT_URL and QDRANT_API_KEY are correct
- **No results**: Check that the collection name matches your Qdrant collection
- **Low relevance**: This may indicate issues with embedding quality
- **Missing metadata**: Verify that embeddings were created with proper metadata