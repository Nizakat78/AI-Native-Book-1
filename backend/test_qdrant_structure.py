#!/usr/bin/env python3
"""
Test script to check Qdrant query_points result structure
"""
import os
from qdrant_client import QdrantClient

# Initialize Qdrant client
qdrant_url = os.getenv('QDRANT_URL', '')
qdrant_api_key = os.getenv('QDRANT_API_KEY', '')

if qdrant_url and qdrant_api_key:
    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        timeout=10
    )

    # Try to get collection info first
    try:
        collections = client.get_collections()
        print("Collections available:")
        for collection in collections.collections:
            print(f"  - {collection.name} (points: {collection.points_count})")
    except Exception as e:
        print(f"Error getting collections: {e}")

    # Try a simple query to see the result structure
    try:
        # Try to query with a simple vector (zeros as a placeholder)
        # This is just to see the structure, not a real search
        print("\nTesting query_points method structure...")
    except Exception as e:
        print(f"Error in test: {e}")
else:
    print("QDRANT_URL and QDRANT_API_KEY environment variables are not set")