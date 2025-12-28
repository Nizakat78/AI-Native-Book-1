# Data Model: RAG Agent with OpenAI Agents SDK

## Entities

### QueryRequest
**Purpose**: Represents a user query request to the RAG agent
**Fields**:
- `query` (string, required): The user's natural language question
- `conversation_id` (string, optional): Unique identifier for conversation continuity
- `user_id` (string, optional): User identifier (for future extension)

### QueryResponse
**Purpose**: Represents the agent's response to a user query
**Fields**:
- `response` (string, required): The agent's answer to the user's query
- `conversation_id` (string, required): Unique identifier for the conversation
- `sources` (array of Source, required): List of sources used in the response
- `timestamp` (datetime, required): When the response was generated

### Source
**Purpose**: Represents a source document used in the response
**Fields**:
- `url` (string, required): URL of the source document
- `content` (string, required): Relevant content snippet from the source
- `relevance_score` (float, required): Relevance score from semantic search
- `section` (string, optional): Section title of the content

### Conversation
**Purpose**: Represents a conversation session with context
**Fields**:
- `conversation_id` (string, required): Unique identifier for the conversation
- `created_at` (datetime, required): When the conversation started
- `last_updated` (datetime, required): When the conversation was last used
- `history` (array of Message, required): Query-response history

### Message
**Purpose**: Represents a single message in a conversation
**Fields**:
- `role` (string, required): "user" or "assistant"
- `content` (string, required): The message content
- `timestamp` (datetime, required): When the message was created

### RetrievalResult
**Purpose**: Represents the results from the Qdrant semantic search
**Fields**:
- `content` (string, required): The retrieved text content
- `url` (string, required): URL of the source document
- `section` (string, optional): Section title
- `chunk_index` (integer, optional): Index of the content chunk
- `score` (float, required): Relevance score from the search
- `metadata` (object, optional): Additional metadata from Qdrant

## Validation Rules

### QueryRequest Validation
- `query` must be non-empty (min length 1)
- `conversation_id` if provided, must be a valid UUID format
- `query` length should be reasonable (max 1000 characters)

### QueryResponse Validation
- `response` must be non-empty
- `sources` array must contain at least one source if response is based on retrieved context
- `conversation_id` must match the UUID format

### Source Validation
- `url` must be a valid URL format
- `content` must be non-empty
- `relevance_score` must be between 0 and 1

## State Transitions

### Conversation States
1. **NEW**: Conversation is created when first query arrives
2. **ACTIVE**: Conversation has ongoing interaction
3. **INACTIVE**: Conversation has not been used for a period (for cleanup)

### Transition Rules
- NEW → ACTIVE: When first response is generated
- ACTIVE → ACTIVE: When additional queries/responses occur
- ACTIVE → INACTIVE: When conversation is not used for 24 hours