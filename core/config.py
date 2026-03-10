import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Nexus AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Firebase Settings
    FIREBASE_CREDENTIALS_PATH: str = os.getenv(
        "FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json"
    )

    # Gemini AI Settings (NO API KEY IN CODE)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL_NAME: str = "gemini-1.5-flash"

    class Config:
        case_sensitive = True


settings = Settings()