from datetime import UTC, datetime
from typing import Any

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass

from .database import Base


class TimestampMixin(MappedAsDataclass):
    """Mixin to add timestamp fields to models."""
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        init=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        init=False,
    )


class SoftDeleteMixin(MappedAsDataclass):
    """Mixin to add soft delete functionality to models."""
    
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False,
    )
    is_deleted: Mapped[bool] = mapped_column(
        nullable=False,
        index=True,
        server_default="false",
        init=False,
    )
