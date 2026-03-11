"""
Production startup script for Nexus AI Backend.
Validates configuration and starts the server safely.
"""

import logging
import sys
from pathlib import Path

# Configure logging early
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def validate_environment():
    """Validate required environment configuration before starting server."""
    logger.info("🔍 Validating environment configuration...")
    
    from core.config import settings
    
    errors = []
    
    # Check critical settings
    if not settings.GEMINI_API_KEY:
        errors.append("❌ GEMINI_API_KEY is not set in environment variables")
    
    # Check Firebase credentials file
    if not Path(settings.FIREBASE_CREDENTIALS_PATH).exists():
        errors.append(
            f"❌ Firebase credentials file not found: {settings.FIREBASE_CREDENTIALS_PATH}"
        )
    
    if errors:
        for error in errors:
            logger.error(error)
        logger.error("\n📝 Please check your .env file and try again")
        return False
    
    logger.info("✅ Environment validation passed!")
    return True


def main():
    """Start the Nexus AI Backend server."""
    import uvicorn
    from core.config import settings
    
    # Validate configuration
    if not validate_environment():
        sys.exit(1)
    
    logger.info(f"🚀 Starting Nexus AI Backend ({settings.VERSION})")
    logger.info(f"📡 Server: http://{settings.SERVER_HOST}:{settings.SERVER_PORT}")
    logger.info(f"🔧 Environment: {settings.PROJECT_NAME}")
    logger.info(f"🤖 AI Model: {settings.GEMINI_MODEL_NAME}")
    
    # Start server
    try:
        uvicorn.run(
            "main:app",
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
            log_level=settings.LOG_LEVEL,
            reload=settings.DEBUG,
        )
    except KeyboardInterrupt:
        logger.info("⛔ Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
