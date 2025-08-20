from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Base Item schema with common fields."""
    title: str = Field(..., min_length=1, max_length=100, description="Item title")
    description: Optional[str] = Field(None, description="Item description")
    price: float = Field(..., ge=0, description="Item price")


class ItemCreate(ItemBase):
    """Schema for creating a new item."""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating an existing item."""
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Item title")
    description: Optional[str] = Field(None, description="Item description")
    price: Optional[float] = Field(None, ge=0, description="Item price")


class ItemRead(ItemBase):
    """Schema for reading item data."""
    id: int = Field(..., description="Item ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True
