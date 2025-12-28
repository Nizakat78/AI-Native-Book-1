# Data Model: RAG Chatbot Integration

## Entity: UserQuery

### Description
Represents a user's question submitted to the RAG chatbot system.

### Fields
- **query_text** (String, required): The main question or query text from the user
- **selected_text** (String, optional): Text selected by the user on the current page for contextual queries
- **context_mode** (Enum, required): The mode of context to use ('full_book' or 'selected_text')
- **user_id** (String, optional): Identifier for the user (for future session tracking)
- **timestamp** (DateTime, required): When the query was submitted
- **metadata** (Object, optional): Additional request metadata (user agent, page context, etc.)

### Validation Rules
- query_text must be between 1 and 1000 characters
- context_mode must be one of the allowed enum values
- If selected_text is provided, context_mode should typically be 'selected_text'

## Entity: QueryResponse

### Description
Represents the system's response to a user's query, including the generated answer and source information.

### Fields
- **response_text** (String, required): The generated response text
- **sources** (Array of Objects, optional): List of sources used in generating the response
  - **source_id** (String): Unique identifier for the source
  - **content** (String): The source content snippet
  - **page_reference** (String): Reference to the original page/document
- **processing_time** (Number, required): Time taken to process the query in milliseconds
- **status** (Enum, required): Processing status ('success', 'error', 'timeout')
- **error_message** (String, optional): Error details if status is 'error'
- **timestamp** (DateTime, required): When the response was generated

### Validation Rules
- response_text must be provided when status is 'success'
- processing_time must be a positive number
- sources should be properly formatted objects when provided

## Entity: ChatSession (Future Extension)

### Description
Represents a conversation session between a user and the chatbot (for future implementation).

### Fields
- **session_id** (String, required): Unique identifier for the session
- **user_id** (String, optional): Identifier for the user
- **created_at** (DateTime, required): When the session was created
- **last_activity** (DateTime, required): When the session was last active
- **messages** (Array of Objects, required): List of messages in the session
  - **role** (Enum): 'user' or 'assistant'
  - **content** (String): The message content
  - **timestamp** (DateTime): When the message was created

### Validation Rules
- session_id must be unique
- messages array must not exceed size limits (for future rate limiting)

## Entity: RetrievalContext

### Description
Represents the context used for document retrieval in the RAG system.

### Fields
- **context_type** (Enum, required): Type of context ('full_book', 'selected_text', 'custom')
- **context_text** (String, optional): The text to use as retrieval context
- **retrieval_strategy** (Enum, required): How to retrieve documents ('semantic', 'keyword', 'hybrid')
- **max_results** (Number, required): Maximum number of documents to retrieve
- **similarity_threshold** (Number, optional): Minimum similarity score for retrieved documents

### Validation Rules
- context_type must be one of the allowed values
- max_results must be between 1 and 10
- similarity_threshold must be between 0 and 1 if provided

## Relationships

### UserQuery → QueryResponse
- One-to-one relationship: Each query generates one response
- QueryResponse references the UserQuery that generated it

### UserQuery → RetrievalContext
- One-to-one relationship: Each query uses one retrieval context
- UserQuery's context_mode and selected_text inform the RetrievalContext

## State Transitions

### Query Processing States
1. **PENDING**: Query received, waiting for processing
2. **PROCESSING**: Query being processed by RAG system
3. **RESPONSE_READY**: Response generated and ready to return
4. **ERROR**: Error occurred during processing

### Valid Transitions
- PENDING → PROCESSING
- PROCESSING → RESPONSE_READY
- PROCESSING → ERROR
- PENDING → ERROR