"""v3: create companies, invitation_codes, agreements tables

Revision ID: 2113c6a59675
Revises: 569557fa3971
Create Date: 2026-03-23 17:52:20.009833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2113c6a59675'
down_revision: Union[str, Sequence[str], None] = '569557fa3971'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
