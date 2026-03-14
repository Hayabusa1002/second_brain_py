import uuid
import enum
from datetime import datetime, UTC

from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.account_owner import account_owners

class AccountType(str, enum.Enum):
    individual = "individual"
    shared = "shared"

class Account(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(Enum(AccountType), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    owners = relationship("User", secondary=account_owners, back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")