"""
Data models for RAG Agent with OpenAI Agents SDK integration.

This module defines the Pydantic models for requests, responses, and data entities
based on the data model specification.
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid


class Source(BaseModel):
    """Represents a source document used in the response."""
    url: str = Field(..., description="URL of the source document")
    content: str = Field(..., description="Relevant content snippet from the source")
    relevance_score: float = Field(..., description="Relevance score from semantic search", ge=0.0, le=1.0)
    section: Optional[str] = Field(None, description="Section title of the content")


class Message(BaseModel):
    """Represents a single message in a conversation."""
    role: str = Field(..., description="Role of the message sender", pattern="^(user|assistant)$")
    content: str = Field(..., description="The message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the message was created")


class QueryRequest(BaseModel):
    """Represents a user query request to the RAG agent."""
    query: str = Field(..., min_length=1, max_length=1000, description="The user's natural language question")
    conversation_id: Optional[str] = Field(None, description="Unique identifier for conversation continuity")

    @validator('conversation_id')
    def validate_conversation_id(cls, v):
        if v is not None:
            try:
                uuid.UUID(v)
            except ValueError:
                raise ValueError('conversation_id must be a valid UUID')
        return v


class QueryResponse(BaseModel):
    """Represents the agent's response to a user query."""
    response: str = Field(..., description="The agent's answer to the user's query")
    conversation_id: str = Field(..., description="Unique identifier for the conversation")
    sources: List[Source] = Field(..., description="List of sources used in the response")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the response was generated")


class Conversation(BaseModel):
    """Represents a conversation session with context."""
    conversation_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the conversation")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the conversation started")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="When the conversation was last used")
    history: List[Message] = Field(default=[], description="Query-response history")


class RetrievalResult(BaseModel):
    """Represents the results from the Qdrant semantic search."""
    content: str = Field(..., description="The retrieved text content")
    url: str = Field(..., description="URL of the source document")
    section: Optional[str] = Field(None, description="Section title")
    chunk_index: Optional[int] = Field(None, description="Index of the content chunk")
    score: float = Field(..., description="Relevance score from the search")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata from Qdrant")