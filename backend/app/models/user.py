from sqlalchemy import Column, String, Enum as SAEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from datetime import datetime, UTC

from app.db.base import Base


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
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.partner)
    status = Column(SAEnum(UserStatus), nullable=False, default=UserStatus.pending)
    oauth_provider = Column(String, nullable=True)
    oauth_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    # back_populates must match exactly the property name on the other model
    accounts = relationship("Account", secondary="account_owners", back_populates="owners")
    transactions = relationship(
        "Transaction",
        back_populates="creator",
        foreign_keys="Transaction.created_by",
        cascade="all, delete-orphan"
    )