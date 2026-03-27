import uuid
import enum
from datetime import datetime, UTC

from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base

class TransactionType(str, enum.Enum):
    income  = "income"
    expense = "expense"

class Transaction(Base):
    __tablename__ = "transactions"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id  = Column(UUID(as_uuid=True), ForeignKey("accounts.id"),    nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"),  nullable=False)
    created_by  = Column(UUID(as_uuid=True), ForeignKey("users.id"),       nullable=False)
    amount      = Column(Numeric(12, 2), nullable=False)
    type        = Column(Enum(TransactionType), nullable=False)
    description = Column(String, nullable=True)
    date        = Column(Date, nullable=False)
    created_at  = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    # back_populates must match exactly the property name on the other model
    account  = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    creator = relationship("User", back_populates="transactions", foreign_keys=[created_by])