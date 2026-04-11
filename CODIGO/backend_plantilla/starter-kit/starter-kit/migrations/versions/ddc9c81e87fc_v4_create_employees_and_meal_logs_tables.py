"""v4: create employees and meal_logs tables

Revision ID: ddc9c81e87fc
Revises: 2113c6a59675
Create Date: 2026-03-23 17:52:40.087034

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddc9c81e87fc'
down_revision: Union[str, Sequence[str], None] = '2113c6a59675'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
