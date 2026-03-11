"""
Constants module for Nexus AI Backend.
Defines application-wide constants and configuration values.
"""


class TaskStatus:
    """Task status constants."""
    
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class AIConfig:
    """AI model configuration constants."""
    
    DEFAULT_PROMPT_PREFIX = (
        "As the Nexus AI Project Manager, "
        "please analyze the following requirement: "
    )
    MAX_OUTPUT_TOKENS = 1000
    TEMPERATURE = 0.7
    
    # Default values for API calls
    TIMEOUT_SECONDS = 30
    MAX_RETRIES = 3