"""add pending to userstatus enum

Revision ID: 9b39d54acecd
Revises: 5a2a3c288ae7
Create Date: 2026-03-18 23:09:31.889441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b39d54acecd'
down_revision: Union[str, Sequence[str], None] = '5a2a3c288ae7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE userstatus ADD VALUE IF NOT EXISTS 'pending';")


def downgrade() -> None:
    """Downgrade schema."""
    pass
