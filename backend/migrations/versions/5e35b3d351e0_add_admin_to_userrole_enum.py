"""add admin to userrole enum

Revision ID: 5e35b3d351e0
Revises: 9b39d54acecd
Create Date: 2026-03-18 23:28:33.672509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e35b3d351e0'
down_revision: Union[str, Sequence[str], None] = '9b39d54acecd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'admin';")


def downgrade() -> None:
    """Downgrade schema."""
    pass
