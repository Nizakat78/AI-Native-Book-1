# Quickstart: RAG Agent with OpenAI Agents SDK

## Overview
This guide will help you set up and run the RAG agent service that integrates OpenAI Agents SDK with Qdrant retrieval for AI textbook content.

## Prerequisites
- Python 3.12+
- OpenAI API key
- Qdrant Cloud URL and API key
- Cohere API key
- uv package manager

## Setup

### 1. Environment Configuration
Create a `.env` file in the backend directory:
```bash
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
QDRANT_COLLECTION=rag_embeddings
```

### 2. Dependencies Installation
```bash
cd backend
uv sync
```

### 3. Service Initialization
```bash
# Run the service
uv run python src/rag_agent/main.py

# Or with uvicorn for development
uv run uvicorn src/rag_agent.main:app --reload --host 0.0.0.0 --port 8000
```

## Usage Examples

### 1. Query the Agent
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key components of humanoid robotics?",
    "conversation_id": "optional-uuid-if-continuing-conversation"
  }'
```

### 2. Start New Conversation
```bash
curl -X POST http://localhost:8000/api/v1/conversations
```

### 3. Get Conversation History
```bash
curl -X GET http://localhost:8000/api/v1/conversations/your-conversation-uuid
```

## Key Components

### Agent Configuration
- System prompt enforces context grounding
- Retrieval tool registered for Qdrant queries
- Response validation ensures source citations

### Retrieval Process
1. User query is received via API
2. Query is embedded using Cohere
3. Semantic search performed in Qdrant
4. Top-k relevant chunks retrieved with metadata
5. Agent generates response using retrieved context

## Validation Steps

### 1. Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### 2. Basic Query Test
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is AI robotics?"}'
```

### 3. Verify Response Grounding
- Check that responses include sources
- Verify sources match the query context
- Confirm responses are relevant to the documentation

## Troubleshooting

### Common Issues
- **API Keys**: Ensure all required API keys are set in environment
- **Qdrant Connection**: Verify Qdrant URL and API key are correct
- **Rate Limits**: Monitor API usage to avoid rate limiting

### Service Status
- Check that all external services (OpenAI, Qdrant, Cohere) are accessible
- Verify the service logs for any connection errors
- Confirm that embeddings exist in Qdrant collection