"""
FastAPI application for RAG chatbot integration.
This module defines the API endpoints for processing user queries.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time
import logging

from .models import UserQuery, QueryResponse, HealthResponse
from .agent import RAGAgent
from .config import config
from .deployment_config import deployment_config
from .utils import validate_query, validate_selected_text, format_api_response, handle_error

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="RAG Chatbot API",
    description="API for processing user queries against book content using RAG",
    version="1.0.0",
    debug=deployment_config.DEBUG
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=deployment_config.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the RAG Agent
rag_agent = RAGAgent()

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {
        "status": "ok",
        "timestamp": time.time()
    }

@app.post("/api/query", response_model=QueryResponse)
@limiter.limit(deployment_config.RATE_LIMIT_DEFAULT)
async def query_endpoint(user_query: UserQuery):
    """
    Process a user query against book content using RAG.

    Args:
        user_query: The query object containing the question and context

    Returns:
        QueryResponse with the answer and sources
    """
    start_time = time.time()

    try:
        # Validate inputs
        if not validate_query(user_query.query):
            raise HTTPException(status_code=400, detail="Invalid query provided")

        if user_query.selected_text and not validate_selected_text(user_query.selected_text):
            raise HTTPException(status_code=400, detail="Invalid selected text provided")

        # Process the query based on context mode
        if user_query.context_mode == "selected_text" and user_query.selected_text:
            response_text, sources = await rag_agent.query_selected_text(
                user_query.query,
                user_query.selected_text
            )
        else:
            response_text, sources = await rag_agent.query_full_book(user_query.query)

        processing_time = time.time() - start_time

        # Format response
        formatted_sources = [Source(**src) if isinstance(src, dict) else src for src in sources]

        return QueryResponse(
            response=response_text,
            sources=formatted_sources,
            processing_time=processing_time,
            status="success"
        )

    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Error processing query: {str(e)}", exc_info=True)

        return QueryResponse(
            response=f"Sorry, I encountered an error processing your query: {str(e)}",
            sources=[],
            processing_time=processing_time,
            status="error",
            error_message=str(e)
        )