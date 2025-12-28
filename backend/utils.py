"""
Utility functions for the RAG chatbot system.
This module contains helper functions for validation, formatting, and common operations.
"""
from typing import Dict, Any, Optional
import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_query(query: str) -> bool:
    """
    Validate the user query.

    Args:
        query: The user's query string

    Returns:
        True if query is valid, False otherwise
    """
    if not query or not isinstance(query, str):
        return False

    query = query.strip()

    # Check if query is not empty
    if not query:
        return False

    # Check length (reasonable limits)
    if len(query) > 1000:
        return False

    return True

def validate_selected_text(selected_text: Optional[str]) -> bool:
    """
    Validate the selected text.

    Args:
        selected_text: The selected text string (optional)

    Returns:
        True if selected text is valid or None, False otherwise
    """
    if selected_text is None:
        return True

    if not isinstance(selected_text, str):
        return False

    selected_text = selected_text.strip()

    # Check length (reasonable limits)
    if len(selected_text) > 5000:  # Reasonable limit for selected text
        return False

    return True

def format_api_response(data: Dict[str, Any], status: str = "success") -> Dict[str, Any]:
    """
    Format a consistent API response.

    Args:
        data: The response data
        status: The status of the response ("success", "error", "timeout")

    Returns:
        Formatted response dictionary
    """
    return {
        "status": status,
        "data": data,
        "timestamp": __import__('time').time()
    }

def sanitize_input(text: str) -> str:
    """
    Sanitize input text to prevent injection attacks.

    Args:
        text: The input text to sanitize

    Returns:
        Sanitized text
    """
    if not text:
        return text

    # Remove potentially dangerous characters/sequences
    # This is a basic sanitization - in production, use more robust methods
    sanitized = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'vbscript:', '', sanitized, flags=re.IGNORECASE)

    return sanitized

def calculate_processing_time(start_time: float) -> float:
    """
    Calculate the processing time from start time to now.

    Args:
        start_time: The start time (from time.time())

    Returns:
        Processing time in seconds
    """
    current_time = __import__('time').time()
    return round(current_time - start_time, 3)


class PerformanceMonitor:
    """
    Utility class for monitoring and tracking performance metrics.
    """

    def __init__(self):
        self.metrics = {}

    def start_timer(self, operation_name: str) -> float:
        """
        Start a timer for a specific operation.

        Args:
            operation_name: Name of the operation being timed

        Returns:
            Start time for the operation
        """
        start_time = __import__('time').time()
        logger.info(f"Starting timer for operation: {operation_name}")
        return start_time

    def stop_timer(self, operation_name: str, start_time: float) -> float:
        """
        Stop a timer for a specific operation and record the duration.

        Args:
            operation_name: Name of the operation that was timed
            start_time: The start time of the operation

        Returns:
            Duration of the operation in seconds
        """
        duration = calculate_processing_time(start_time)
        logger.info(f"Operation '{operation_name}' took {duration:.3f} seconds")

        # Store metrics for monitoring
        if operation_name not in self.metrics:
            self.metrics[operation_name] = []
        self.metrics[operation_name].append(duration)

        return duration

    def get_average_duration(self, operation_name: str) -> float:
        """
        Get the average duration for an operation.

        Args:
            operation_name: Name of the operation

        Returns:
            Average duration in seconds
        """
        if operation_name in self.metrics and self.metrics[operation_name]:
            durations = self.metrics[operation_name]
            avg_duration = sum(durations) / len(durations)
            return round(avg_duration, 3)
        return 0.0

    def get_metrics_summary(self) -> Dict[str, Dict[str, float]]:
        """
        Get a summary of all performance metrics.

        Returns:
            Dictionary with metrics summary for each operation
        """
        summary = {}
        for operation_name, durations in self.metrics.items():
            if durations:
                summary[operation_name] = {
                    "count": len(durations),
                    "average": round(sum(durations) / len(durations), 3),
                    "min": round(min(durations), 3),
                    "max": round(max(durations), 3),
                    "total": round(sum(durations), 3)
                }
        return summary


# Global performance monitor instance
performance_monitor = PerformanceMonitor()

class APIError(Exception):
    """
    Custom exception for API-related errors.
    """
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def handle_error(error: Exception, logger: logging.Logger) -> Dict[str, Any]:
    """
    Handle an error and return a formatted error response.

    Args:
        error: The exception that occurred
        logger: The logger to use for logging the error

    Returns:
        Formatted error response
    """
    logger.error(f"API Error: {str(error)}", exc_info=True)

    return format_api_response(
        {
            "error": str(error),
            "type": type(error).__name__
        },
        status="error"
    )