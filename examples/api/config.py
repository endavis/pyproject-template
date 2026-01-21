"""Application configuration using Pydantic Settings.

Configuration is loaded from environment variables with sensible defaults
for development. In production, set these via environment variables or .env file.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "Example API"
    version: str = "1.0.0"
    debug: bool = True

    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
