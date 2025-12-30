"""
Agent module for the RAG chatbot system.
This module handles the processing of user queries and generation of responses.
"""
from typing import Dict, List, Optional, Tuple
import logging
import asyncio
import time
import httpx
from openai import OpenAI, OpenAIError
from .retrieval import RetrievalService
from .models import Source
from .config import config
from .cache import query_cache
from .utils import performance_monitor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGAgent:
    """
    RAG Agent class to handle query processing and response generation.
    """

    def __init__(self):
        """
        Initialize the RAG agent with necessary services.
        """
        logger.info("Initializing RAG Agent")
        self.retrieval_service = RetrievalService()
        self.openai_client = OpenAI(
            api_key=config.OPENAI_API_KEY,
            timeout=30.0  # 30 second timeout for API calls
        )

    async def process_query(self, query: str, context_mode: str = "full_book", selected_text: Optional[str] = None) -> Tuple[str, List[Dict]]:
        """
        Process a user query and generate a response.

        Args:
            query: The user's query
            context_mode: Either "full_book" or "selected_text"
            selected_text: Optional selected text for context

        Returns:
            Tuple of (response_text, list_of_sources)
        """
        # Start performance monitoring
        start_time = performance_monitor.start_timer("query_processing")

        # Check cache first to optimize response time
        cached_result = query_cache.get(query, context_mode, selected_text)
        if cached_result:
            logger.info(f"Cache hit for query: '{query[:50]}...'")
            # Record performance for cached response
            performance_monitor.stop_timer("query_processing", start_time)
            return cached_result

        try:
            # Retrieve relevant documents based on context mode
            retrieval_start = performance_monitor.start_timer("document_retrieval")
            retrieved_docs = await self.retrieval_service.retrieve_documents(
                query, context_mode, selected_text
            )
            performance_monitor.stop_timer("document_retrieval", retrieval_start)

            # Generate response using OpenAI
            generation_start = performance_monitor.start_timer("response_generation")
            response_text = await self._generate_response(query, retrieved_docs)
            performance_monitor.stop_timer("response_generation", generation_start)

            # Format sources
            sources = []
            for doc in retrieved_docs:
                sources.append({
                    "id": doc.get("id", ""),
                    "content": doc.get("content", "")[:200],  # Truncate for display
                    "page_reference": doc.get("page_reference", "")
                })

            # Calculate total processing time
            total_time = performance_monitor.stop_timer("query_processing", start_time)
            logger.info(f"Query processed in {total_time:.2f} seconds")

            # Cache the result if it's not an error response (to avoid caching errors)
            if not response_text.startswith("Sorry, I encountered an error"):
                query_cache.set(query, (response_text, sources), context_mode=context_mode, selected_text=selected_text)

            return response_text, sources

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}", exc_info=True)
            total_time = performance_monitor.stop_timer("query_processing", start_time)
            error_response = f"Sorry, I encountered an error processing your query: {str(e)}"
            return error_response, []

    async def query_full_book(self, query: str) -> Tuple[str, List[Dict]]:
        """
        Process a query against the full book content.

        Args:
            query: The user's query

        Returns:
            Tuple of (response_text, list_of_sources)
        """
        return await self.process_query(query, "full_book")

    async def query_selected_text(self, query: str, selected_text: str) -> Tuple[str, List[Dict]]:
        """
        Process a query with focus on selected text context.

        Args:
            query: The user's query
            selected_text: The selected text for context

        Returns:
            Tuple of (response_text, list_of_sources)
        """
        return await self.process_query(query, "selected_text", selected_text)

    async def _generate_response(self, query: str, retrieved_docs: List[Dict]) -> str:
        """
        Generate a response using OpenAI based on the query and retrieved documents.

        Args:
            query: The user's query
            retrieved_docs: List of retrieved documents to use as context

        Returns:
            Generated response text
        """
        # Build context from retrieved documents
        context_text = ""
        for doc in retrieved_docs:
            content = doc.get("content", "")
            if content:
                context_text += f"Context: {content}\n\n"

        # Build the prompt for OpenAI
        prompt = f"""
        You are an AI assistant for a Physical AI and Humanoid Robotics textbook.
        Answer the user's question based on the provided context.

        Context:
        {context_text}

        User Question: {query}

        Please provide a helpful and accurate response based on the context provided.
        If the context doesn't contain relevant information, please say so.
        """

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",  # Using a more accessible model
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            return "Sorry, I'm having trouble generating a response right now. Please try again later."

    async def query_full_book(self, query: str) -> Tuple[str, List[Dict]]:
        """
        Process a query against the full book content.

        Args:
            query: The user's query

        Returns:
            Tuple of (response_text, list_of_sources)
        """
        return await self.process_query(query, "full_book")

    async def query_selected_text(self, query: str, selected_text: str) -> Tuple[str, List[Dict]]:
        """
        Process a query with focus on selected text context.

        Args:
            query: The user's query
            selected_text: The selected text for context

        Returns:
            Tuple of (response_text, list_of_sources)
        """
        return await self.process_query(query, "selected_text", selected_text)