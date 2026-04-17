"""Application configuration using pydantic-settings."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Global application settings loaded from environment / .env file."""

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_TITLE: str = "SportClub Order Management System"
    APP_VERSION: str = "0.1.0"

    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'app.db'}"

    # CORS – allow frontend dev server
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]


settings = Settings()
