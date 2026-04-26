from datetime import datetime, UTC

from sqlalchemy import Table, Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


store_subcategories = Table(
    "store_subcategories",
    Base.metadata,
    Column("store_id", UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), primary_key=True),
    Column("subcategory_id", UUID(as_uuid=True), ForeignKey("subcategories.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)),
    Column("created_by", UUID(as_uuid=True), ForeignKey("users.id"), nullable=True),
    Column("updated_at", DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)),
    Column("updated_by", UUID(as_uuid=True), ForeignKey("users.id"), nullable=True),
)