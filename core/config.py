"""
Configuration module for Nexus AI Backend.
Handles environment variables and application settings.
"""

import os
from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv()


class Settings(BaseSettings):
    """Application settings with validation."""
    
    # Project Info
    PROJECT_NAME: str = "Nexus AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Firebase Settings
    FIREBASE_CREDENTIALS_PATH: str = os.getenv(
        "FIREBASE_CREDENTIALS_PATH", 
        "serviceAccountKey.json"
    )

    # Gemini AI Settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL_NAME: str = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")

    # Server Settings
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info").lower()

    class Config:
        """Pydantic configuration."""
        case_sensitive = True
        env_file = ".env"
        extra = "allow"


# Create settings instance
try:
    settings = Settings()
    
    # Validate critical settings
    if not settings.GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is not set. "
            "Please set it in your .env file or environment variables."
        )
except ValueError as e:
    raise RuntimeError(f"Configuration Error: {e}")