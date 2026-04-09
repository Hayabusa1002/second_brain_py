import uuid
import enum
from datetime import datetime, UTC

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.store_subcategory import store_subcategories


class StoreType(str, enum.Enum):
    physical = "physical"
    online = "online"
    subscription = "subscription"
    service = "service"


class Store(Base):
    __tablename__ = "stores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(120), nullable=False)
    type = Column(Enum(StoreType, name="store_type"), nullable=False)
    address = Column(String(200), nullable=True)
    website = Column(String(200), nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # 1:N with transactions
    transactions = relationship("Transaction", back_populates="store")

    # N:N with subcategories
    subcategories = relationship("Subcategory", secondary=store_subcategories, back_populates="stores")