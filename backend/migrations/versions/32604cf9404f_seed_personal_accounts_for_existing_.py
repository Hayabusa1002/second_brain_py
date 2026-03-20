"""seed personal accounts for existing users

Revision ID: 32604cf9404f
Revises: 5e35b3d351e0
Create Date: 2026-03-19 23:45:36.957392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = '32604cf9404f'
down_revision: Union[str, Sequence[str], None] = '5e35b3d351e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    users = conn.execute(sa.text("""
        SELECT u.id
        FROM users u
        LEFT JOIN accounts a
            ON a.created_by = u.id AND a.type = 'individual'
        WHERE a.id IS NULL
    """)).fetchall()

    for row in users:
        user_id = str(row[0])
        account_id = str(uuid.uuid4())

        conn.execute(sa.text("""
            INSERT INTO accounts (id, name, type, created_by, created_at)
            VALUES (:id, 'Personal', 'individual', :created_by, NOW())
        """), {"id": account_id, "created_by": user_id})

        conn.execute(sa.text("""
            INSERT INTO account_owners (account_id, user_id)
            VALUES (:account_id, :user_id)
        """), {"account_id": account_id, "user_id": user_id})


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()

    conn.execute(sa.text("""
        DELETE FROM account_owners
        WHERE account_id IN (
            SELECT id FROM accounts
            WHERE name = 'Personal' AND type = 'individual'
        )
    """))

    conn.execute(sa.text("""
        DELETE FROM accounts
        WHERE name = 'Personal' AND type = 'individual'
    """))
