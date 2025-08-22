from enum import Enum
from typing import Any, Optional

from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings

from app.schemas.language_models import (
    AllModelEnum,
    FakeModelName,
    Provider,
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

    APP_NAME: str = Field(default="FRAI Boilerplate", description="Application name")
    APP_DESCRIPTION: str = Field(
        default="A production-ready FRAI boilerplate",
        description="Application description",
    )
    APP_VERSION: str = Field(default="0.1.0", description="Application version")
    DEBUG: bool = Field(default=True, description="Debug mode")
    RELOAD: bool = Field(default=True, description="Auto-reload on code changes")


class DatabaseSettings(BaseSettings):
    """Database connection settings."""

    POSTGRES_USER: str = Field(default="postgres", description="PostgreSQL username")
    POSTGRES_PASSWORD: str = Field(
        default="postgres", description="PostgreSQL password"
    )
    POSTGRES_SERVER: str = Field(
        default="localhost", description="PostgreSQL server host"
    )
    POSTGRES_PORT: int = Field(default=5432, description="PostgreSQL server port")
    POSTGRES_DB: str = Field(default="frai_db", description="PostgreSQL database name")

    # Test database settings
    POSTGRES_TEST_DB: str = Field(
        default="frai_test_db", description="PostgreSQL test database name"
    )

    @property
    def POSTGRES_ASYNC_URL(self) -> str:
        """Build async PostgreSQL URL."""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def POSTGRES_TEST_ASYNC_URL(self) -> str:
        """Build async PostgreSQL test database URL."""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_TEST_DB}"


class LanguageModelSettings(BaseSettings):
    """Language model API settings."""

    DEFAULT_MODEL: AllModelEnum = Field(
        default=AnthropicModelName.HAIKU_3, description="Default language model"
    )
    ANTHROPIC_API_KEY: Optional[str] = Field(
        default=None, description="Anthropic API key"
    )
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API key")
    

    @property
    def has_anthropic_api_key(self) -> bool:
        """Check if Anthropic API key is available."""
        return bool(self.ANTHROPIC_API_KEY)

    @property
    def has_openai_api_key(self) -> bool:
        """Check if OpenAI API key is available."""
        return bool(self.OPENAI_API_KEY)

    def model_post_init(self, __context: Any) -> None:
        api_keys = {
            Provider.ANTHROPIC: self.ANTHROPIC_API_KEY,
            Provider.OPENAI: self.OPENAI_API_KEY,
        }

        active_keys = [k for k, v in api_keys.items() if v]
        if not active_keys:
            raise ValueError("At least one LLM API key must be provided.")

        for provider in active_keys:
            match provider:
                case Provider.OPENAI:
                    if self.DEFAULT_MODEL is None:
                        self.DEFAULT_MODEL = OpenAIModelName.GPT_4O_MINI
                    self.AVAILABLE_MODELS.update(set(OpenAIModelName))
                case Provider.ANTHROPIC:
                    if self.DEFAULT_MODEL is None:
                        self.DEFAULT_MODEL = AnthropicModelName.HAIKU_3
                    self.AVAILABLE_MODELS.update(set(AnthropicModelName))
                case Provider.FAKE:
                    if self.DEFAULT_MODEL is None:
                        self.DEFAULT_MODEL = FakeModelName.FAKE
                    self.AVAILABLE_MODELS.update(set(FakeModelName))
                case _:
                    raise ValueError(f"Unknown provider: {provider}")


class Settings(AppSettings, DatabaseSettings, LanguageModelSettings):
    """Main settings class combining all configuration."""

    ENVIRONMENT: EnvironmentOption = Field(
        default=EnvironmentOption.DEVELOPMENT, description="Application environment"
    )

    @property
    def DATABASE_URL(self) -> str:
        """Get the appropriate database URL based on environment."""
        if self.ENVIRONMENT == EnvironmentOption.TESTING:
            return self.POSTGRES_TEST_ASYNC_URL
        return self.POSTGRES_ASYNC_URL

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

    model_config = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


# Global settings instance
settings = Settings()
