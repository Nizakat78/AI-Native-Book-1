#!/usr/bin/env python3
"""
Simple test script to verify basic agent functionality.
"""
import sys
import os

# Add the backend src to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

def test_basic_agent():
    """Test basic agent functionality with simple queries."""
    try:
        from backend.src.rag_agent.agent import RAGAgent
        from backend.src.rag_agent.retrieval_tool import QdrantRetrievalTool

        print("Initializing retrieval tool...")
        retrieval_tool = QdrantRetrievalTool()
        print("✓ Retrieval tool initialized successfully")

        print("Initializing RAG agent...")
        agent = RAGAgent()
        print("✓ RAG agent initialized successfully")

        print("Setting retrieval tool...")
        agent.set_retrieval_tool(retrieval_tool)
        print("✓ Retrieval tool set successfully")

        print("Testing query functionality...")
        test_query = "What is AI robotics?"
        response, sources = agent.query_with_sources(test_query)

        print(f"✓ Query processed successfully")
        print(f"Response: {response[:100]}...")  # First 100 chars
        print(f"Sources found: {len(sources)}")

        agent.cleanup()
        print("✓ Agent cleaned up successfully")

        print("\n✓ All basic agent functionality tests passed!")
        return True

    except Exception as e:
        print(f"✗ Error during basic agent test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_agent()
    if not success:
        sys.exit(1)