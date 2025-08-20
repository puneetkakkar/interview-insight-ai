import os
from enum import Enum
from typing import Optional

from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class EnvironmentOption(str, Enum):
    """Environment options for the application."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class AppSettings(BaseSettings):
    """Application settings."""
    APP_NAME: str = Field(default="FRAI Boilerplate", description="Application name")
    APP_DESCRIPTION: str = Field(default="A production-ready FRAI boilerplate", description="Application description")
    APP_VERSION: str = Field(default="0.1.0", description="Application version")
    DEBUG: bool = Field(default=True, description="Debug mode")
    RELOAD: bool = Field(default=True, description="Auto-reload on code changes")


class DatabaseSettings(BaseSettings):
    """Database connection settings."""
    POSTGRES_USER: str = Field(default="postgres", description="PostgreSQL username")
    POSTGRES_PASSWORD: str = Field(default="postgres", description="PostgreSQL password")
    POSTGRES_SERVER: str = Field(default="localhost", description="PostgreSQL server host")
    POSTGRES_PORT: int = Field(default=5432, description="PostgreSQL server port")
    POSTGRES_DB: str = Field(default="frai_db", description="PostgreSQL database name")
    
    # Test database settings
    POSTGRES_TEST_DB: str = Field(default="frai_test_db", description="PostgreSQL test database name")
    
    @property
    def POSTGRES_ASYNC_URL(self) -> str:
        """Build async PostgreSQL URL."""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def POSTGRES_TEST_ASYNC_URL(self) -> str:
        """Build async PostgreSQL test database URL."""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_TEST_DB}"


class SecuritySettings(BaseSettings):
    """Security settings."""
    SECRET_KEY: str = Field(default="your-secret-key-here-change-in-production", description="Secret key for JWT")
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")


class Settings(AppSettings, DatabaseSettings, SecuritySettings):
    """Main settings class combining all configuration."""
    ENVIRONMENT: EnvironmentOption = Field(default=EnvironmentOption.DEVELOPMENT, description="Application environment")
    
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
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# Global settings instance
settings = Settings()
