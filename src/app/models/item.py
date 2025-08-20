from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base
from ..core.db.models import TimestampMixin, SoftDeleteMixin


class Item(Base, TimestampMixin, SoftDeleteMixin):
    """Example Item model for demonstration."""
    
    __tablename__ = "items"
    
    # Fields without defaults must come first
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(nullable=False, default=0.0)
    
    # Mixin fields with defaults will be added automatically
    
    def __repr__(self) -> str:
        return f"<Item(id={self.id}, title='{self.title}', price={self.price})>"
