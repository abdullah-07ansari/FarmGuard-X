import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "FarmGuard X AI API"
    VERSION: str = "1.0.0"
    MODEL_VERSION: str = "MobileNetV3-PlantVillage-v1.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "farmguard_secret_key_super_secure_change_in_production_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/farmguard.db"
    
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    RECOMMENDATIONS_FILE: Path = BASE_DIR / "app" / "data" / "recommendations.json"

    class Config:
        case_sensitive = True

settings = Settings()

# Ensure required runtime directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.RECOMMENDATIONS_FILE.parent, exist_ok=True)
