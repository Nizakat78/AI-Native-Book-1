"""
Caching module for the RAG chatbot system.
This module provides caching functionality for frequently asked questions.
"""
from typing import Dict, Optional, Any
import time
import hashlib
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    """
    Represents a cached entry with its data and expiration time.
    """
    data: Any
    created_at: float
    ttl: float  # Time to live in seconds

    def is_expired(self) -> bool:
        """
        Check if the cache entry is expired.

        Returns:
            True if expired, False otherwise
        """
        return time.time() - self.created_at > self.ttl

    def time_remaining(self) -> float:
        """
        Get the time remaining before expiration.

        Returns:
            Time remaining in seconds
        """
        return max(0, self.ttl - (time.time() - self.created_at))


class QueryCache:
    """
    In-memory cache for storing frequently asked questions and their responses.
    """

    def __init__(self, default_ttl: float = 3600):  # 1 hour default TTL
        """
        Initialize the query cache.

        Args:
            default_ttl: Default time-to-live for cache entries in seconds
        """
        self.default_ttl = default_ttl
        self._cache: Dict[str, CacheEntry] = {}
        self._access_count: Dict[str, int] = {}
        logger.info(f"QueryCache initialized with default TTL: {default_ttl}s")

    def _generate_key(self, query: str, context_mode: str = "full_book", selected_text: Optional[str] = None) -> str:
        """
        Generate a unique cache key for a query.

        Args:
            query: The user's query
            context_mode: The context mode
            selected_text: The selected text (if any)

        Returns:
            Unique cache key
        """
        key_data = f"{query}:{context_mode}:{selected_text or ''}"
        return hashlib.sha256(key_data.encode()).hexdigest()

    def get(self, query: str, context_mode: str = "full_book", selected_text: Optional[str] = None) -> Optional[Any]:
        """
        Get a cached response for a query.

        Args:
            query: The user's query
            context_mode: The context mode
            selected_text: The selected text (if any)

        Returns:
            Cached response if found and not expired, None otherwise
        """
        key = self._generate_key(query, context_mode, selected_text)

        if key in self._cache:
            entry = self._cache[key]

            if entry.is_expired():
                logger.info(f"Cache entry expired for key: {key[:8]}...")
                del self._cache[key]
                if key in self._access_count:
                    del self._access_count[key]
                return None

            # Update access count
            self._access_count[key] = self._access_count.get(key, 0) + 1

            logger.info(f"Cache hit for key: {key[:8]}...")
            return entry.data

        logger.info(f"Cache miss for key: {key[:8]}...")
        return None

    def set(self, query: str, response: Any, ttl: Optional[float] = None, context_mode: str = "full_book", selected_text: Optional[str] = None):
        """
        Store a response in the cache.

        Args:
            query: The user's query
            response: The response to cache
            ttl: Time-to-live for this specific entry (uses default if None)
            context_mode: The context mode
            selected_text: The selected text (if any)
        """
        if ttl is None:
            ttl = self.default_ttl

        key = self._generate_key(query, context_mode, selected_text)
        entry = CacheEntry(
            data=response,
            created_at=time.time(),
            ttl=ttl
        )

        self._cache[key] = entry
        self._access_count[key] = 1

        logger.info(f"Cache set for key: {key[:8]}... with TTL: {ttl}s")

    def delete(self, query: str, context_mode: str = "full_book", selected_text: Optional[str] = None) -> bool:
        """
        Delete a specific cache entry.

        Args:
            query: The user's query
            context_mode: The context mode
            selected_text: The selected text (if any)

        Returns:
            True if entry was deleted, False if not found
        """
        key = self._generate_key(query, context_mode, selected_text)

        if key in self._cache:
            del self._cache[key]
            if key in self._access_count:
                del self._access_count[key]
            logger.info(f"Cache entry deleted for key: {key[:8]}...")
            return True

        return False

    def clear(self):
        """
        Clear all cache entries.
        """
        self._cache.clear()
        self._access_count.clear()
        logger.info("Cache cleared")

    def cleanup_expired(self) -> int:
        """
        Remove all expired entries from the cache.

        Returns:
            Number of entries removed
        """
        initial_count = len(self._cache)
        expired_keys = [key for key, entry in self._cache.items() if entry.is_expired()]

        for key in expired_keys:
            del self._cache[key]
            if key in self._access_count:
                del self._access_count[key]

        removed_count = initial_count - len(self._cache)
        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} expired cache entries")

        return removed_count

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        total_entries = len(self._cache)
        expired_count = len([entry for entry in self._cache.values() if entry.is_expired()])
        non_expired_count = total_entries - expired_count

        # Calculate average TTL of non-expired entries
        active_entries = [entry for entry in self._cache.values() if not entry.is_expired()]
        avg_ttl = sum(entry.ttl for entry in active_entries) / len(active_entries) if active_entries else 0

        return {
            "total_entries": total_entries,
            "non_expired_entries": non_expired_count,
            "expired_entries": expired_count,
            "average_ttl": avg_ttl,
            "most_accessed_keys": sorted(self._access_count.items(), key=lambda x: x[1], reverse=True)[:5]
        }

    def get_cache_size(self) -> int:
        """
        Get the current number of cache entries.

        Returns:
            Number of cache entries
        """
        return len(self._cache)


# Global cache instance
query_cache = QueryCache(default_ttl=1800)  # 30 minutes default TTL