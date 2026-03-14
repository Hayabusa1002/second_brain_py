from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


account_owners = Table(
    "account_owners",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("account_id", UUID(as_uuid=True), ForeignKey("accounts.id"), primary_key=True),
)