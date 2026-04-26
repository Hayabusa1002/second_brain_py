import uuid
from datetime import datetime, UTC

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.store_subcategory import store_subcategories


class Subcategory(Base):
    __tablename__ = "subcategories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(80), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # N:1 with category
    category = relationship("Category", back_populates="subcategories")

    # 1:N with transactions
    transactions = relationship("Transaction", back_populates="subcategory")

    # N:N with stores
    stores = relationship("Store", secondary=store_subcategories, back_populates="subcategories")

    # 1:N with items
    items = relationship("Item", back_populates="subcategory")