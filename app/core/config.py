import os
from typing import List
from urllib.parse import urlparse, urlunparse
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the project root directory (flash-full folder)
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=(
            "backend/backend.env",
            "backend.env",
            "backend/.env",
            ".env",
        ),
        case_sensitive=True,
        extra="ignore",
    )
    
    # Application
    APP_NAME: str = "Flash ERP"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    RUN_STARTUP_TASKS: bool = True
    
    # Database (will be overridden below)
    DATABASE_URL: str = ""

    # Uploads (legacy local path)
    UPLOADS_DIR: str = os.path.join(_PROJECT_ROOT, "uploads")
    
    # Backblaze B2 Storage
    B2_KEY_ID: str = "005840bd883f2c00000000003"
    B2_APPLICATION_KEY: str = "K0052OPof6wSuwuRGVX7uyOElwfMMwI"
    B2_BUCKET_NAME: str = "flash-erp-new"
    B2_ENDPOINT_URL: str = "https://s3.us-east-005.backblazeb2.com"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001,http://127.0.0.1:3001,http://localhost:8000,http://127.0.0.1:8000"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Convert comma-separated string to list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()


def _redact_database_url(database_url: str) -> str:
    """Hide sensitive info in logs."""
    try:
        parsed = urlparse(database_url)
        if parsed.scheme.startswith("sqlite"):
            return database_url
        if parsed.username:
            host = parsed.hostname or ""
            port = f":{parsed.port}" if parsed.port else ""
            netloc = f"{parsed.username}:***@{host}{port}"
            return urlunparse(parsed._replace(netloc=netloc))
        return database_url
    except Exception:
        return "<redacted>"


# Remote PostgreSQL database configuration
USER = os.getenv("DB_USER", "postgres")
PASSWORD = os.getenv("DB_PASSWORD", "c7Od03Arvx4Aix3rl9sxPcFyrJWOZVYW6sakZ00zK54i32bT3eSEgcNPekjom1oe")
HOST = os.getenv("DB_HOST", "46.202.194.55")
DBNAME = os.getenv("DB_NAME", "flashnew")
PORT = os.getenv("DB_PORT", "5432")

# Construct DATABASE_URL if not provided in environment
if not settings.DATABASE_URL:
    settings.DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
elif "postgresql://" in settings.DATABASE_URL and "asyncpg" not in settings.DATABASE_URL:
    # Ensure it uses asyncpg driver if provided as standard postgres://
    settings.DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

print(f"[Config] Using database: {_redact_database_url(settings.DATABASE_URL)}")
