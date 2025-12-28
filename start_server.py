#!/usr/bin/env python3
"""
Startup script for RAG Agent API
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

# Add backend/src to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

# Now run the main application
from rag_agent.main import app
import uvicorn

if __name__ == "__main__":
    from rag_agent.config import get_config
    config = get_config()
    uvicorn.run(app, host=config.host, port=config.port)