import uuid
import enum
from datetime import datetime, UTC

from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.account_owner import account_owners


class UserRole(str, enum.Enum):
    admin = "admin"
    owner = "owner"
    partner = "partner"


class UserStatus(str, enum.Enum):
    active = "active"
    pending = "pending"
    inactive = "inactive"
    banned = "banned"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=True)
    role = Column(Enum(UserRole, name="user_type"), nullable=False, default=UserRole.partner)
    status = Column(Enum(UserStatus, name="user_status"), nullable=False, default=UserStatus.pending)
    oauth_provider = Column(String, nullable=True)
    oauth_id = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # N:N with accounts
    accounts = relationship("Account", secondary=account_owners, back_populates="owners")

    # 1:N with transactions
    transactions = relationship(
        "Transaction",
        back_populates="creator",
        foreign_keys="Transaction.created_by",
    )

    # 1:N with paid_transactions
    paid_transactions = relationship(
        "Transaction",
        back_populates="payer",
        foreign_keys="Transaction.paid_by",
    )

    # 1:N with received_transactions
    received_transactions = relationship(
        "Transaction",
        back_populates="payee",
        foreign_keys="Transaction.paid_to",
    )