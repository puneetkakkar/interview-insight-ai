# The application primarily uses direct SQLAlchemy operations.
# Consider using repositories for more complex database operations or remove if not needed.

# CRUD Operations

from .base import BaseRepository

__all__ = ["BaseRepository"]
