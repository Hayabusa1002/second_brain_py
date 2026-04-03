import uuid
from datetime import datetime, UTC

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Store(Base):
    __tablename__ = "stores"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name       = Column(String(120), nullable=False)
    category   = Column(String(80), nullable=True)
    address    = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    transactions = relationship(
        "Transaction",
        back_populates="store",
        foreign_keys="Transaction.store_id",
    )