import uuid
import enum
from datetime import datetime, UTC

from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class TransactionType(str, enum.Enum):
    income = "income"
    expense = "expense"


class PaymentMethod(str, enum.Enum):
    cash = "cash"
    debit = "debit"
    credit = "credit"
    transfer = "transfer"


class Transaction(Base):
    __tablename__ = "transactions"

    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id     = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    store_id       = Column(UUID(as_uuid=True), ForeignKey("stores.id"), nullable=True)
    category_id    = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    subcategory_id = Column(UUID(as_uuid=True), ForeignKey("subcategories.id"), nullable=True)
    city_id        = Column(UUID(as_uuid=True), ForeignKey("cities.id"), nullable=True)

    type           = Column(Enum(TransactionType, name="transaction_type"), nullable=False)
    payment_method = Column(Enum(PaymentMethod, name="payment_method"), nullable=False)
    amount         = Column(Numeric(12, 2), nullable=False)
    description    = Column(String, nullable=True)
    date           = Column(Date, nullable=False)
    created_at     = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    created_by     = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    paid_by        = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    paid_to        = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    account        = relationship("Account", back_populates="transactions")
    store          = relationship("Store", back_populates="transactions", foreign_keys=[store_id])
    category       = relationship("Category", back_populates="transactions")
    subcategory    = relationship("Subcategory", back_populates="transactions")
    city           = relationship("City", back_populates="transactions")

    creator        = relationship("User", back_populates="transactions", foreign_keys=[created_by])
    payer          = relationship("User", back_populates="paid_transactions", foreign_keys=[paid_by])
    payee          = relationship("User", back_populates="received_transactions", foreign_keys=[paid_to])

    items          = relationship(
        "TransactionItem",
        back_populates="transaction",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )