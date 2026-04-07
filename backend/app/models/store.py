import uuid
from enum import Enum
from datetime import datetime, UTC

from sqlalchemy import Column, DateTime, Enum as SqlEnum, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class StoreType(str, Enum):
    physical = "physical"
    online = "online"
    subscription = "subscription"
    service = "service"


class Store(Base):
    __tablename__ = "stores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(120), nullable=False)
    type = Column(
        SqlEnum(StoreType, name="store_type"),
        nullable=False,
    )
    address = Column(String(200), nullable=True)
    website = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    transactions = relationship(
        "Transaction",
        back_populates="store",
        foreign_keys="Transaction.store_id",
    )

    category_default = relationship(
        "StoreCategoryDefault",
        back_populates="store",
        uselist=False,
        cascade="all, delete-orphan",
    )


class StoreCategoryDefault(Base):
    __tablename__ = "store_category_defaults"
    __table_args__ = (
        UniqueConstraint("store_id", name="uq_store_category_defaults_store_id"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_id = Column(
        UUID(as_uuid=True),
        ForeignKey("stores.id", ondelete="cascade"),
        nullable=False,
    )
    subcategory_id = Column(
        UUID(as_uuid=True),
        ForeignKey("subcategories.id", ondelete="cascade"),
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    store = relationship("Store", back_populates="category_default")
    subcategory = relationship("Subcategory", back_populates="store_category_defaults")