"""Add qr_token to employees and total_amount to meal_logs

Revision ID: abc1234567def89
Revises: 8a9c8d7e4f3b
Create Date: 2026-04-04 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abc1234567def89'
down_revision: Union[str, Sequence[str], None] = '8a9c8d7e4f3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add qr_token to employees
    op.add_column('employees', sa.Column('qr_token', sa.String(), nullable=True, unique=True))
    
    # Add total_amount to meal_logs
    op.add_column('meal_logs', sa.Column('total_amount', sa.Float(), nullable=False, server_default='0.0'))


def downgrade() -> None:
    """Downgrade schema."""
    # Drop total_amount from meal_logs
    op.drop_column('meal_logs', 'total_amount')
    
    # Drop qr_token from employees
    op.drop_column('employees', 'qr_token')
