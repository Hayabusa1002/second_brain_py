import uuid
from datetime import datetime, UTC

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Subcategory(Base):
    __tablename__ = "subcategories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(80), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    category = relationship("Category", back_populates="subcategories")
    transactions = relationship("Transaction", back_populates="subcategory")
    store_subcategories = relationship("StoreSubcategory", back_populates="subcategory")
    items = relationship("TransactionItem", back_populates="subcategory")