"""v1: create users table

Revision ID: 07a52fcd5c15
Revises: 04c59698a962
Create Date: 2026-03-23 17:51:58.685750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07a52fcd5c15'
down_revision: Union[str, Sequence[str], None] = '04c59698a962'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
