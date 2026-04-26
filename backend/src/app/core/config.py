from enum import Enum
from pathlib import Path
from typing import Any, Optional

from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings

# Resolve .env path relative to this file so it works regardless of CWD.
# config.py lives at: backend/src/app/core/config.py
# .env lives at:      backend/.env  (4 levels up)
_ENV_FILE = Path(__file__).resolve().parent.parent.parent.parent / ".env"

from src.app.schemas.language_models import (
    AllModelEnum,
    FakeModelName,
    OpenAIModelName,
    AnthropicModelName,
)


class EnvironmentOption(str, Enum):
    """Environment options for the application."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class AppSettings(BaseSettings):
    """Application settings."""

    APP_NAME: str = Field(default="CandidateSignal", description="Application name")
    APP_DESCRIPTION: str = Field(
        default="A production-ready AI-powered interview transcript analysis platform",
        description="Application description",
    )
    APP_VERSION: str = Field(default="1.0.0", description="Application version")
    ENVIRONMENT: str = Field(default="development", description="Environment")
    DEBUG: bool = Field(default=True, description="Debug mode")
    RELOAD: bool = Field(default=True, description="Auto-reload mode")
    LOG_LEVEL: str = Field(default="INFO", description="Log level")
    DEBUG_TOOLS_OUTPUT: bool = Field(default=False, description="Save debug output for each tool execution")

    @property
    def IS_TESTING(self) -> bool:
        """Check if running in testing environment."""
        return self.ENVIRONMENT == EnvironmentOption.TESTING

    @property
    def IS_DEVELOPMENT(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == EnvironmentOption.DEVELOPMENT

    @property
    def IS_PRODUCTION(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == EnvironmentOption.PRODUCTION


class DatabaseSettings(BaseSettings):
    """Database connection settings."""

    STORAGE_TYPE: str = Field(
        default="postgres", description="Storage type: postgres or memory"
    )
    POSTGRES_SERVER: str = Field(default="localhost", description="PostgreSQL server")
    POSTGRES_PORT: int = Field(default=5432, description="PostgreSQL port")
    POSTGRES_DB: str = Field(
        default="candidate_signal_db", description="PostgreSQL database name"
    )
    POSTGRES_USER: str = Field(default="postgres", description="PostgreSQL username")
    POSTGRES_PASSWORD: str = Field(
        default="postgres", description="PostgreSQL password"
    )
    POSTGRES_TEST_DB: str = Field(
        default="candidate_signal_test_db", description="PostgreSQL test database name"
    )

    @property
    def POSTGRES_ASYNC_URL(self) -> str:
        """Build async PostgreSQL URL."""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def POSTGRES_TEST_ASYNC_URL(self) -> str:
        """Build async PostgreSQL test database URL."""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_TEST_DB}"

    @property
    def is_memory_storage(self) -> bool:
        """Check if using in-memory storage."""
        return self.STORAGE_TYPE.lower() == "memory"

    @property
    def is_postgres_storage(self) -> bool:
        """Check if using PostgreSQL storage."""
        return self.STORAGE_TYPE.lower() == "postgres"


class LanguageModelSettings(BaseSettings):
    """Language model API settings."""

    DEFAULT_MODEL: AllModelEnum = Field(
        default=AnthropicModelName.HAIKU_3, description="Default language model"
    )
    ANTHROPIC_API_KEY: Optional[str] = Field(
        default=None, description="Anthropic API key"
    )
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API key")
    OPENWEATHERMAP_API_KEY: Optional[str] = Field(
        default=None, description="OpenWeatherMap API key"
    )
    USE_LLM_CACHE: bool = Field(default=True, description="Use LLM cache")

    @property
    def has_anthropic_api_key(self) -> bool:
        """Check if Anthropic API key is available."""
        return bool(self.ANTHROPIC_API_KEY)

    @property
    def has_openai_api_key(self) -> bool:
        """Check if OpenAI API key is available."""
        return bool(self.OPENAI_API_KEY)

    @property
    def available_models(self) -> set:
        """Get available models based on API keys."""
        models = set()

        if self.ANTHROPIC_API_KEY:
            models.update(set(AnthropicModelName))

        if self.OPENAI_API_KEY:
            models.update(set(OpenAIModelName))

        if not models:  # If no API keys, add fake model for testing
            models.add(FakeModelName.FAKE)

        return models

    def model_post_init(self, __context: Any) -> None:
        """Validate that at least one API key is provided."""
        # Allow running without API keys for development/testing
        # The application will use mocked responses when no API keys are available
        pass


class Settings(AppSettings, DatabaseSettings, LanguageModelSettings):
    """Main application settings that combines all other setting classes."""

    @property
    def DATABASE_URL(self) -> str:
        """Get the appropriate database URL based on environment and storage type."""
        if DatabaseSettings.is_memory_storage:
            return "sqlite+aiosqlite:///:memory:"
        elif self.IS_TESTING:
            return DatabaseSettings.POSTGRES_TEST_ASYNC_URL
        return DatabaseSettings.POSTGRES_ASYNC_URL

    model_config = ConfigDict(
        env_file=str(_ENV_FILE), env_file_encoding="utf-8", case_sensitive=True
    )


# Global settings instance
settings = Settings()
