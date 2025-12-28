"""
RAG Agent orchestration module (Third-Party Model Only).

Uses OpenRouter free models (NO OpenAI paid dependency).
"""

import os
import uuid
import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple

from agents import Agent, Runner
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI

from .models import RetrievalResult, Source
from .tools import retrieve_content

logger = logging.getLogger(__name__)

# ============================
# THIRD-PARTY MODEL (OPENROUTER)
# ============================

# Create AsyncOpenAI client for OpenRouter
openai_client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

# Correct model initialization (latest SDK)
third_party_model = OpenAIChatCompletionsModel(
    openai_client=openai_client,
    model="mistralai/devstral-2512:free"
)

# ============================
# RAG AGENT
# ============================

class RAGAgent:
    """
    RAG Agent using ONLY third-party FREE LLM via OpenRouter.
    """

    _conversations: Dict[str, Dict[str, Any]] = {}

    def __init__(self):
        # We retrieve content manually before passing to the agent
        # so we don't need to include tools in the agent itself
        self.retrieval_tool = retrieve_content

        self.agent_instructions = """
You are an AI assistant for an AI textbook on Physical AI and Humanoid Robotics.

RULES:
- Answer ONLY from provided context
- Do NOT use outside knowledge
- Cite sources
- If context missing, say you don't know
- Audience: advanced CS & Robotics students
"""

        self.agent = Agent(
            name="RAG Textbook Assistant",
            instructions=self.agent_instructions,
            model=third_party_model,
            # Note: We handle retrieval manually, so no tools needed here
            tools=[],
        )

        logger.info("✅ RAG Agent initialized with OpenRouter FREE model")

    # ============================
    # Conversation Helpers
    # ============================

    def create_conversation(self) -> str:
        cid = str(uuid.uuid4())
        self._conversations[cid] = {"history": []}
        return cid

    def add_message(self, cid: str, role: str, content: str):
        if cid in self._conversations:
            self._conversations[cid]["history"].append(
                {"role": role, "content": content}
            )

    # ============================
    # Core Query Logic
    # ============================

    async def query_with_sources_async(
        self,
        user_query: str,
    ) -> Tuple[str, List[Source]]:
        """
        Async version of query_with_sources for use in async contexts like FastAPI.
        """
        import asyncio
        import concurrent.futures

        def run_sync_query():
            # Call the sync version in a separate thread
            return self.query_with_sources(user_query)

        # Run the synchronous version in a thread pool to avoid async conflicts
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            response, sources = await loop.run_in_executor(executor, run_sync_query)
            return response, sources

    def query_with_sources(
        self,
        user_query: str,
    ) -> Tuple[str, List[Source]]:
        """
        Synchronous version of query_with_sources for use in sync contexts.
        """
        try:
            # For our RAG implementation, we need to call the retrieval function directly
            # to get the context before passing to the agent
            # Using the internal function to bypass the tool decoration
            from .tools import _internal_retrieve_content

            retrieved = _internal_retrieve_content(user_query, top_k=5)

            context_text = ""
            sources: List[Source] = []

            if retrieved:
                context_text += "Context from textbook:\n\n"

                for i, item in enumerate(retrieved):
                    # Since retrieve_content returns Dict objects, not RetrievalResult
                    if isinstance(item, dict):
                        context_text += f"[{i+1}] {item.get('content', '')}\n\n"
                        sources.append(
                            Source(
                                url=item.get('url', ''),
                                content=item.get('content', '')[:200],
                                relevance_score=item.get('score', 0.0),
                                section=item.get('section', ''),
                            )
                        )

            final_prompt = (
                f"{context_text}\nQuestion:\n{user_query}"
                if context_text
                else user_query
            )

            # Use the synchronous version of the agent runner
            response = self._run_agent_sync(final_prompt)

            if not response:
                response = "No relevant information found in the textbook."

            return response, sources

        except Exception as e:
            logger.exception("RAG query failed")
            return f"Error: {str(e)}", []

    # ============================
    # Async Runner Wrapper
    # ============================

    def _run_agent_sync(self, prompt: str) -> str:
        """Synchronous version of the agent runner."""
        import asyncio
        import threading
        import concurrent.futures

        # Run the async method in a separate thread to avoid event loop conflicts
        def run_in_new_loop():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                return new_loop.run_until_complete(self._run_async(prompt))
            finally:
                new_loop.close()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_in_new_loop)
            return future.result()

    async def _run_async(self, prompt: str) -> str:
        result = await Runner.run(self.agent, prompt)

        if hasattr(result, "final_output"):
            return result.final_output

        return str(result)

    # ============================
    # Public API
    # ============================

    async def process_async(
        self,
        query: str,
        conversation_id: Optional[str] = None,
    ) -> Tuple[str, List[Source], str]:
        """
        Async version of process for use in async contexts like FastAPI.
        """
        if not conversation_id:
            conversation_id = self.create_conversation()

        self.add_message(conversation_id, "user", query)

        answer, sources = await self.query_with_sources_async(query)

        self.add_message(conversation_id, "assistant", answer)

        return answer, sources, conversation_id

    def process(
        self,
        query: str,
        conversation_id: Optional[str] = None,
    ) -> Tuple[str, List[Source], str]:
        """
        Synchronous version of process for use in sync contexts.
        """
        if not conversation_id:
            conversation_id = self.create_conversation()

        self.add_message(conversation_id, "user", query)

        answer, sources = self.query_with_sources(query)

        self.add_message(conversation_id, "assistant", answer)

        return answer, sources, conversation_id

    def get_conversation_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Get the history for a specific conversation.

        Args:
            conversation_id: The conversation ID

        Returns:
            List of message dictionaries
        """
        if conversation_id in self._conversations:
            return self._conversations[conversation_id]['history']
        return []

    def cleanup(self):
        logger.info("RAG Agent cleaned up")
