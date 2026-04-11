"""v2: create restaurants table

Revision ID: 569557fa3971
Revises: 07a52fcd5c15
Create Date: 2026-03-23 17:52:07.805728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '569557fa3971'
down_revision: Union[str, Sequence[str], None] = '07a52fcd5c15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
