# API Contracts: RAG Agent with OpenAI Agents SDK

## Overview
RESTful API endpoints for the RAG agent service that integrates OpenAI Agents SDK with Qdrant retrieval.

## Base URL
`/api/v1`

## Authentication
None required for initial implementation (will be added in future specs)

## Endpoints

### POST /query
**Purpose**: Submit a user query to the RAG agent and receive a response

**Request**:
```json
{
  "query": "What are the key components of humanoid robotics?",
  "conversation_id": "optional-conversation-uuid"
}
```

**Response** (200 OK):
```json
{
  "response": "The key components of humanoid robotics include the mechanical structure, actuators, sensors, control systems, and AI algorithms...",
  "conversation_id": "unique-conversation-uuid",
  "sources": [
    {
      "url": "https://ai-native-book-1.vercel.app/docs/humanoid-robotics-modules/spec",
      "content": "On this page Feature Branch : 1-humanoid-robotics-modules Created : 2025-12-21 Status : Draft Input : User description: \"Project: AI-native textbook on Physical AI Humanoid Robotics Target audience: C...",
      "relevance_score": 0.85
    }
  ],
  "timestamp": "2025-12-26T12:00:00Z"
}
```

**Validation**:
- `query` is required and must be 1-1000 characters
- `conversation_id` if provided, must be a valid UUID

**Error Responses**:
- 400: Bad Request - Invalid request format
- 422: Unprocessable Entity - Validation failed
- 500: Internal Server Error - Agent or retrieval service failure

### GET /conversations/{conversation_id}
**Purpose**: Retrieve conversation history for a specific conversation

**Path Parameters**:
- `conversation_id`: UUID of the conversation

**Response** (200 OK):
```json
{
  "conversation_id": "unique-conversation-uuid",
  "created_at": "2025-12-26T10:00:00Z",
  "last_updated": "2025-12-26T12:00:00Z",
  "history": [
    {
      "role": "user",
      "content": "What are the key components of humanoid robotics?",
      "timestamp": "2025-12-26T12:00:00Z"
    },
    {
      "role": "assistant",
      "content": "The key components of humanoid robotics include...",
      "timestamp": "2025-12-26T12:00:05Z"
    }
  ]
}
```

**Error Responses**:
- 404: Not Found - Conversation does not exist
- 500: Internal Server Error

### POST /conversations
**Purpose**: Start a new conversation

**Request**: Empty body or optionally include initial context

**Response** (201 Created):
```json
{
  "conversation_id": "newly-generated-conversation-uuid",
  "created_at": "2025-12-26T12:00:00Z"
}
```

### GET /health
**Purpose**: Health check endpoint to verify service status

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2025-12-26T12:00:00Z",
  "services": {
    "openai_agent": "connected",
    "qdrant_retrieval": "connected",
    "cohere_embeddings": "available"
  }
}
```

## Error Format
All error responses follow this format:
```json
{
  "error": {
    "type": "error_type",
    "message": "Human-readable error message",
    "details": "Additional error details if applicable"
  }
}
```

## Common Error Types
- `invalid_request`: Request format or validation error
- `retrieval_error`: Error during Qdrant retrieval
- `agent_error`: Error during agent processing
- `service_unavailable`: External service unavailable