"""
Data models for the RAG chatbot system.
This module defines the Pydantic models for requests and responses.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
import time

class ContextMode(str, Enum):
    """
    Enum for context modes.
    """
    full_book = "full_book"
    selected_text = "selected_text"

class UserQuery(BaseModel):
    """
    Model for user query requests.
    """
    query: str = Field(..., description="The user's question", min_length=1, max_length=1000)
    selected_text: Optional[str] = Field(None, description="Optional selected text for context", max_length=5000)
    context_mode: ContextMode = Field(default=ContextMode.full_book, description="Query context type")

    class Config:
        use_enum_values = True

class Source(BaseModel):
    """
    Model for source citations in responses.
    """
    id: str = Field(..., description="Unique identifier for the source")
    content: str = Field(..., description="Content snippet from the source", max_length=2000)
    page_reference: Optional[str] = Field(None, description="Reference to the original page/document")

class QueryResponse(BaseModel):
    """
    Model for query responses.
    """
    response: str = Field(..., description="The generated response", min_length=1)
    sources: List[Source] = Field(default_factory=list, description="List of sources used")
    processing_time: float = Field(..., description="Time taken to process query in seconds")
    status: str = Field(default="success", description="Processing status")
    error_message: Optional[str] = Field(None, description="Error details if status is 'error'")

    class Config:
        use_enum_values = True

class HealthResponse(BaseModel):
    """
    Model for health check responses.
    """
    status: str = Field(default="ok", description="Health status")
    timestamp: float = Field(default_factory=time.time, description="When the health check was performed")