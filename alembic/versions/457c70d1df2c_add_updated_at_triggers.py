"""add updated_at triggers

Revision ID: 457c70d1df2c
Revises: 19fd7fe49f1f
Create Date: 2026-09-08 12:33:46.637250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '457c70d1df2c'
down_revision: Union[str, Sequence[str], None] = '19fd7fe49f1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

tables = ['users', 'clients', 'memberships']

def upgrade() -> None:
    """Upgrade schema."""
    op.execute('''
        CREATE OR REPLACE FUNCTION set_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    ''')

    for table in tables:

        op.execute(f'''
            CREATE TRIGGER {table}_set_updated_at
            BEFORE UPDATE ON {table}
            FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        ''')



def downgrade() -> None:
    """Downgrade schema."""

    for table in tables:
        op.execute(f'''
            DROP TRIGGER IF EXISTS {table}_set_updated_at ON {table}
        ''')

    op.execute("DROP FUNCTION IF EXISTS set_updated_at()")
    