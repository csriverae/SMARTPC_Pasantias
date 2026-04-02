"""Add ruc field and make restaurant_id nullable

Revision ID: 8a9c8d7e4f3b
Revises: ddc9c81e87fc
Create Date: 2026-04-02 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '8a9c8d7e4f3b'
down_revision: Union[str, Sequence[str], None] = 'ddc9c81e87fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add ruc column to companies table
    op.add_column('companies', sa.Column('ruc', sa.String(), nullable=True))
    
    # Make restaurant_id nullable
    op.alter_column('companies', 'restaurant_id',
               existing_type=sa.Integer(),
               nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Make restaurant_id not nullable again
    op.alter_column('companies', 'restaurant_id',
               existing_type=sa.Integer(),
               nullable=False)
    
    # Drop ruc column
    op.drop_column('companies', 'ruc')
