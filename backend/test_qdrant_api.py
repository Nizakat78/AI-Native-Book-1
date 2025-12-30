#!/usr/bin/env python3
"""
Test script to check QdrantClient API methods
"""
from qdrant_client import QdrantClient

# Create a client instance (without connecting to check methods)
client = QdrantClient

# Print available methods
print("Available QdrantClient methods:")
methods = [method for method in dir(QdrantClient) if not method.startswith('_')]
for method in sorted(methods):
    print(f"  {method}")

print("\nSearching for search-related methods:")
search_methods = [method for method in dir(QdrantClient) if 'search' in method.lower()]
for method in search_methods:
    print(f"  {method}")