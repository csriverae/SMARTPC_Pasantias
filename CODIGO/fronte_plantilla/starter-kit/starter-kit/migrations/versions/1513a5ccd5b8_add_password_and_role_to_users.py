"""add password and role to users

Revision ID: 1513a5ccd5b8
Revises: ddc9c81e87fc
Create Date: 2026-03-24 17:40:09.954194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1513a5ccd5b8'
down_revision: Union[str, Sequence[str], None] = 'ddc9c81e87fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('password', sa.String(), nullable=False))
    op.add_column('users', sa.Column('role', sa.Enum('admin', 'restaurant_admin', 'company_admin', 'employee', name='userrole'), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'role')
    op.drop_column('users', 'password')
