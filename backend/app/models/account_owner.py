from datetime import datetime, UTC

from sqlalchemy import Table, Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


account_owners = Table(
    "account_owners",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("account_id", UUID(as_uuid=True), ForeignKey("accounts.id"), primary_key=True),
    Column("created_at", DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)),
    Column("created_by", UUID(as_uuid=True), ForeignKey("users.id"), nullable=True),
    Column("updated_at", DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)),
    Column("updated_by", UUID(as_uuid=True), ForeignKey("users.id"), nullable=True),
)