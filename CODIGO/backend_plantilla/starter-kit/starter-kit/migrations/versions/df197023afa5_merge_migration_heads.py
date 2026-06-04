"""merge migration heads

Revision ID: df197023afa5
Revises: add_saas_columns_001, mobile_device_sessions
Create Date: 2026-06-03 20:05:47.444034

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df197023afa5'
down_revision: Union[str, Sequence[str], None] = ('add_saas_columns_001', 'mobile_device_sessions')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
