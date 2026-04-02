import uuid

from sqlalchemy import Column, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class TransactionItem(Base):
    __tablename__ = "items"

    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("transactions.id", ondelete="CASCADE"),
        nullable=False,
    )
    name           = Column(String(150), nullable=False)
    quantity       = Column(Numeric(10, 2), nullable=False, default=1)
    unit_price     = Column(Numeric(12, 2), nullable=False)
    subtotal       = Column(Numeric(12, 2), nullable=False)
    notes          = Column(Text, nullable=True)

    transaction = relationship("Transaction", back_populates="items")