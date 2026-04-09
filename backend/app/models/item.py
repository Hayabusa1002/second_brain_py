import uuid
from datetime import datetime, UTC

from sqlalchemy import Column, ForeignKey, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    notes = Column(Text, nullable=True)

    subcategory_id = Column(
        UUID(as_uuid=True),
        ForeignKey("subcategories.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # N:1 with subcategory
    subcategory = relationship("Subcategory", back_populates="items")

    # N:N with transactions
    # 1:N with transaction_items (intermediate pivot table but non-pure)
    transaction_items = relationship(
        "TransactionItem",
        back_populates="item",
        cascade="all, delete-orphan",
    )