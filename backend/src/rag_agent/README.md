# RAG Agent with OpenAI Agents SDK

This module implements a RAG (Retrieval-Augmented Generation) agent that integrates OpenAI Agents SDK with Qdrant retrieval for AI textbook content.

## Overview

The RAG agent provides an intelligent interface to query AI textbook content using natural language. It retrieves relevant context from the textbook and generates responses grounded in the provided information.

## API Endpoints

### Health Check
- `GET /health` - Check service health status

### Query Endpoint
- `POST /api/v1/query` - Submit a query to the RAG agent
  - Request body:
    ```json
    {
      "query": "What are the key components of humanoid robotics?",
      "conversation_id": "optional-conversation-uuid"
    }
    ```
  - Response:
    ```json
    {
      "response": "The key components of humanoid robotics include...",
      "conversation_id": "unique-conversation-uuid",
      "sources": [
        {
          "url": "https://example.com/source",
          "content": "Relevant content snippet...",
          "relevance_score": 0.85,
          "section": "optional-section-title"
        }
      ],
      "timestamp": "2025-12-26T12:00:00Z"
    }
    ```

### Conversation Management
- `POST /api/v1/conversations` - Start a new conversation
- `GET /api/v1/conversations/{conversation_id}` - Get conversation history

## Environment Variables

- `OPENAI_API_KEY` - OpenAI API key
- `QDRANT_URL` - Qdrant Cloud URL
- `QDRANT_API_KEY` - Qdrant API key
- `QDRANT_COLLECTION` - Qdrant collection name (default: rag_embeddings)
- `COHERE_API_KEY` - Cohere API key
- `HOST` - Host for the service (default: 0.0.0.0)
- `PORT` - Port for the service (default: 8000)
- `DEBUG` - Debug mode (default: False)

## Usage

To start the service:

```bash
cd backend
uv run python src/rag_agent/main.py
```

Or with uvicorn for development:

```bash
uv run uvicorn src.rag_agent.main:app --reload --host 0.0.0.0 --port 8000
```

## Architecture

- **FastAPI**: Web framework for API endpoints
- **OpenAI Agents SDK**: AI agent orchestration
- **Qdrant**: Vector database for semantic search
- **Cohere**: Embedding generation for retrieval