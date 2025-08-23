from collections.abc import AsyncGenerator
from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

from ..config import settings


class Base(DeclarativeBase, MappedAsDataclass):
    """Base class for all database models."""
    pass


# Initialize engine and session as None
async_engine: Optional[Any] = None
async_session: Optional[Any] = None


def initialize_database() -> None:
    """Initialize database engine and session based on configuration."""
    global async_engine, async_session
    
    if settings.is_memory_storage:
        # Use SQLite in-memory for development/testing
        from sqlalchemy import create_engine
        engine = create_engine("sqlite:///:memory:", echo=settings.DEBUG)
        # For in-memory, we'll use sync engine and create tables immediately
        from ..db.models import Base
        Base.metadata.create_all(bind=engine)
        # Store the sync engine for in-memory mode
        async_engine = engine
        async_session = None
    else:
        # Use PostgreSQL
        async_engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
            future=True,
            pool_pre_ping=True,
        )
        async_session = async_sessionmaker(
            bind=async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session."""
    if settings.is_memory_storage:
        # For in-memory storage, create a sync session and wrap it
        from sqlalchemy.orm import sessionmaker
        
        # Create a sync session factory
        sync_session_factory = sessionmaker(bind=async_engine)
        
        # Create a sync session
        sync_session = sync_session_factory()
        
        # Create a mock async session that delegates to sync session
        class SyncToAsyncSession:
            def __init__(self, sync_session):
                self.sync_session = sync_session
            
            async def execute(self, query):
                # Execute the query synchronously
                result = self.sync_session.execute(query)
                return result
            
            async def commit(self):
                self.sync_session.commit()
            
            async def refresh(self, obj):
                self.sync_session.refresh(obj)
            
            async def close(self):
                self.sync_session.close()
            
            def add(self, obj):
                self.sync_session.add(obj)
        
        async_session_wrapper = SyncToAsyncSession(sync_session)
        try:
            yield async_session_wrapper
        finally:
            await async_session_wrapper.close()
    else:
        # Use PostgreSQL async session
        if async_session is None:
            raise RuntimeError("Database not initialized. Call initialize_database() first.")
        
        async with async_session() as session:
            try:
                yield session
            finally:
                await session.close()


async def init_db() -> None:
    """Initialize database (create tables)."""
    if settings.is_memory_storage:
        # For in-memory storage, tables are created during initialization
        return
    
    if async_engine:
        async with async_engine.begin() as conn:
            # Import all models here to ensure they are registered
            # Note: Models will be imported dynamically based on configuration
            await conn.run_sync(Base.metadata.create_all)
    else:
        raise RuntimeError("Database not initialized. Call initialize_database() first.")


async def close_db() -> None:
    """Close database connections."""
    if async_engine and not settings.is_memory_storage:
        await async_engine.dispose()
