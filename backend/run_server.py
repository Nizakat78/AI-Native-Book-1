#!/usr/bin/env python3
"""
Script to run the RAG agent API server with proper environment loading.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the backend/src directory to the path to allow absolute imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import uvicorn
from src.rag_agent.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)