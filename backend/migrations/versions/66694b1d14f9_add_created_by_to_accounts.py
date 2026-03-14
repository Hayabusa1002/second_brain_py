"""add created_by to accounts

Revision ID: 66694b1d14f9
Revises: eba8a983b38d
Create Date: 2026-03-14 16:16:15.811156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66694b1d14f9'
down_revision: Union[str, Sequence[str], None] = 'eba8a983b38d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Step 1: add as nullable
    op.add_column('accounts', sa.Column('created_by', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'accounts', 'users', ['created_by'], ['id'])

    # Step 2: backfill existing accounts with default user
    op.execute("UPDATE accounts SET created_by = '00000000-0000-0000-0000-000000000099' WHERE created_by IS NULL")

    # Step 3: enforce NOT NULL
    op.alter_column('accounts', 'created_by', nullable=False)

    # Update role column type
    op.alter_column('users', 'role',
               existing_type=sa.VARCHAR(),
               type_=sa.Enum('owner', 'partner', name='userrole'),
               existing_nullable=False,
               postgresql_using='role::userrole')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'role',
               existing_type=sa.Enum('owner', 'partner', name='userrole'),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    op.drop_constraint(None, 'accounts', type_='foreignkey')
    op.drop_column('accounts', 'created_by')
