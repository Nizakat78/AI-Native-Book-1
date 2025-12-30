"""
Deployment configuration for RAG Chatbot API.
This module provides configuration settings for different deployment environments.
"""
import os
from typing import Optional

class DeploymentConfig:
    """
    Configuration class for deployment settings.
    """

    # Environment settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # API settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_WORKERS: int = int(os.getenv("API_WORKERS", "1"))

    # CORS settings for Vercel and GitHub Pages compatibility
    CORS_ORIGINS: list = [
        "http://localhost:3000",      # Local Docusaurus development
        "http://localhost:3001",      # Alternative local dev
        "http://localhost:3002",      # Additional local dev
        "https://*.vercel.app",       # Vercel deployments
        "https://*.github.io",        # GitHub Pages
        "https://*.github.com",       # GitHub Pages preview
    ]

    # Add any additional origins from environment
    ADDITIONAL_CORS_ORIGINS: str = os.getenv("ADDITIONAL_CORS_ORIGINS", "")
    if ADDITIONAL_CORS_ORIGINS:
        CORS_ORIGINS.extend(ADDITIONAL_CORS_ORIGINS.split(","))

    # Rate limiting configuration
    RATE_LIMIT_DEFAULT: str = os.getenv("RATE_LIMIT_DEFAULT", "10/minute")
    RATE_LIMIT_BURST: str = os.getenv("RATE_LIMIT_BURST", "30/minute")

    # Timeout settings
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    CONNECTION_TIMEOUT: int = int(os.getenv("CONNECTION_TIMEOUT", "60"))

    # Health check settings
    HEALTH_CHECK_INTERVAL: int = int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))

    # Cache settings
    CACHE_TTL_DEFAULT: int = int(os.getenv("CACHE_TTL_DEFAULT", "1800"))  # 30 minutes
    CACHE_TTL_LONG: int = int(os.getenv("CACHE_TTL_LONG", "3600"))       # 1 hour
    CACHE_TTL_SHORT: int = int(os.getenv("CACHE_TTL_SHORT", "300"))      # 5 minutes

    # Vercel-specific settings
    VERCEL_ENV: Optional[str] = os.getenv("VERCEL_ENV")  # production, preview, development
    VERCEL_GIT_COMMIT_REF: Optional[str] = os.getenv("VERCEL_GIT_COMMIT_REF")
    VERCEL_PROJECT_NAME: Optional[str] = os.getenv("VERCEL_PROJECT_NAME")
    VERCEL_URL: Optional[str] = os.getenv("VERCEL_URL")

    @classmethod
    def is_production(cls) -> bool:
        """
        Check if running in production environment.

        Returns:
            True if in production, False otherwise
        """
        return cls.ENVIRONMENT.lower() in ["production", "prod"]

    @classmethod
    def is_development(cls) -> bool:
        """
        Check if running in development environment.

        Returns:
            True if in development, False otherwise
        """
        return cls.ENVIRONMENT.lower() in ["development", "dev"]

    @classmethod
    def is_testing(cls) -> bool:
        """
        Check if running in testing environment.

        Returns:
            True if in testing, False otherwise
        """
        return cls.ENVIRONMENT.lower() in ["testing", "test"]

    @classmethod
    def get_cors_origins(cls) -> list:
        """
        Get CORS origins based on environment.

        Returns:
            List of allowed origins
        """
        origins = cls.CORS_ORIGINS.copy()

        # Add additional origins for specific environments
        if cls.is_development():
            origins.extend([
                "http://localhost:*",  # Any localhost port
                "http://127.0.0.1:*",  # Any 127.0.0.1 port
            ])

        return origins


# Global configuration instance
deployment_config = DeploymentConfig()