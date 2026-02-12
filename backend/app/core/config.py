from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

# Get the directory where this config file is located: backend/app/core/config.py
# .parent -> backend/app/core
# .parent.parent -> backend/app
# .parent.parent.parent -> backend
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "Private Knowledge Q&A"
    GOOGLE_API_KEY: str
    ALLOWED_ORIGINS: str = "http://localhost:5173"
    
    # Storage
    STORAGE_FILE: str = "storage.json"
    
    # Model Config
    EMBEDDING_MODEL: str = "gemini-embedding-001"
    CHAT_MODEL: str = "gemini-flash-latest"

    # Use model_config for Pydantic v2
    model_config = {
        "env_file": str(BASE_DIR / ".env"),
        "extra": "ignore"
    }

@lru_cache()
def get_settings():
    return Settings()
