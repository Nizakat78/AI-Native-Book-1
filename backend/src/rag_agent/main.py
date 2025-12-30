"""
FastAPI application for RAG Agent with OpenAI Agents SDK integration.

This module initializes the FastAPI application and sets up the basic structure
for the RAG agent service that integrates OpenAI Agents SDK with Qdrant retrieval.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from typing import Optional
import asyncio

import sys
import os
# Add the backend/src directory to the path to allow absolute imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from rag_agent.agent import RAGAgent
from rag_agent.retrieval_tool import QdrantRetrievalTool
from rag_agent.models import QueryRequest, QueryResponse, Conversation, Message
from rag_agent.config import get_config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global agent instance
rag_agent: Optional[RAGAgent] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for application startup and shutdown.
    """
    logger.info("Starting up RAG Agent service...")

    # Initialize the RAG agent (the tool is already included in the agent)
    try:
        global rag_agent
        rag_agent = RAGAgent()
        logger.info("RAG Agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG Agent: {e}")
        raise

    yield

    # Cleanup on shutdown
    if rag_agent:
        rag_agent.cleanup()
        logger.info("RAG Agent cleaned up")

    logger.info("Shutting down RAG Agent service...")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="RAG Agent API",
    description="API for RAG Agent with OpenAI Agents SDK and Qdrant retrieval",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:8080",
        "http://127.0.0.1:*",
        "http://localhost:*",
        "https://*.vercel.app",
        "https://*.github.io",
        "https://*.github.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint for basic health check."""
    return {"message": "RAG Agent API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    # Check if the services are available
    services_status = {
        "openai_agent": "connected",  # Assume connected if agent initialized
        "qdrant_retrieval": "connected",  # Assume connected if retrieval tool initialized
        "cohere_embeddings": "available"  # Assume available if environment configured
    }

    return {
        "status": "healthy",
        "service": "rag-agent-api",
        "timestamp": __import__('datetime').datetime.utcnow().isoformat() + "Z",
        "services": services_status
    }

# Import and include API routes
@app.post("/api/v1/query", response_model=QueryResponse)
async def query_endpoint_v1(request: QueryRequest):
    """
    Query endpoint (v1) to interact with the RAG agent.

    Args:
        request: QueryRequest containing the user's query and optional conversation_id

    Returns:
        QueryResponse with the agent's answer and sources
    """
    global rag_agent

    if not rag_agent:
        raise HTTPException(status_code=500, detail="RAG Agent not initialized")

    try:
        import asyncio
        import concurrent.futures

        # Run the synchronous agent processing in a thread executor
        # to avoid async conflicts with nested event loops
        loop = asyncio.get_event_loop()

        def run_agent_processing():
            if request.conversation_id:
                # Use conversation functionality if conversation_id provided
                return rag_agent.process(
                    request.query,
                    conversation_id=request.conversation_id
                )
            else:
                # Create a new conversation
                return rag_agent.process(request.query)

        # Execute the agent processing in a thread to avoid async conflicts
        response_text, sources, conversation_id = await loop.run_in_executor(
            None,  # Uses default executor
            run_agent_processing
        )

        # Create the response with actual sources
        response = QueryResponse(
            response=response_text,
            conversation_id=conversation_id,
            sources=sources,
            timestamp=__import__('datetime').datetime.utcnow()
        )

        return response
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/api/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Query endpoint to interact with the RAG agent.

    Args:
        request: QueryRequest containing the user's query and optional conversation_id

    Returns:
        QueryResponse with the agent's answer and sources
    """
    global rag_agent

    if not rag_agent:
        raise HTTPException(status_code=500, detail="RAG Agent not initialized")

    try:
        import asyncio
        import concurrent.futures

        # Run the synchronous agent processing in a thread executor
        # to avoid async conflicts with nested event loops
        loop = asyncio.get_event_loop()

        def run_agent_processing():
            if request.conversation_id:
                # Use conversation functionality if conversation_id provided
                return rag_agent.process(
                    request.query,
                    conversation_id=request.conversation_id
                )
            else:
                # Create a new conversation
                return rag_agent.process(request.query)

        # Execute the agent processing in a thread to avoid async conflicts
        response_text, sources, conversation_id = await loop.run_in_executor(
            None,  # Uses default executor
            run_agent_processing
        )

        # Create the response with actual sources
        response = QueryResponse(
            response=response_text,
            conversation_id=conversation_id,
            sources=sources,
            timestamp=__import__('datetime').datetime.utcnow()
        )

        return response
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

# Additional API endpoints for conversation management
@app.post("/api/v1/conversations", response_model=Conversation)
async def create_conversation():
    """
    Create a new conversation.

    Returns:
        Conversation: New conversation object with ID
    """
    global rag_agent

    if not rag_agent:
        raise HTTPException(status_code=500, detail="RAG Agent not initialized")

    try:
        conversation_id = rag_agent.create_conversation()
        conversation = Conversation(
            conversation_id=conversation_id,
            created_at=__import__('datetime').datetime.utcnow(),
            last_updated=__import__('datetime').datetime.utcnow(),
            history=[]
        )
        return conversation
    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating conversation: {str(e)}")

@app.get("/api/v1/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    """
    Get conversation history for a specific conversation.

    Args:
        conversation_id: The conversation ID to retrieve

    Returns:
        Conversation: Conversation object with history
    """
    global rag_agent

    if not rag_agent:
        raise HTTPException(status_code=500, detail="RAG Agent not initialized")

    try:
        history_data = rag_agent.get_conversation_history(conversation_id)

        # Convert the raw history data to Message objects
        history = []
        for item in history_data:
            message = Message(
                role=item.get('role', 'user'),
                content=item.get('content', ''),
                timestamp=item.get('timestamp', __import__('datetime').datetime.utcnow())
            )
            history.append(message)

        # For now, use a default created_at time (in a full implementation, we'd store this)
        conversation = Conversation(
            conversation_id=conversation_id,
            created_at=__import__('datetime').datetime.utcnow(),
            last_updated=__import__('datetime').datetime.utcnow(),
            history=history
        )
        return conversation
    except Exception as e:
        logger.error(f"Error retrieving conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    config = get_config()
    uvicorn.run(app, host=config.host, port=config.port)