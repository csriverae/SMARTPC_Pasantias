"""merge_heads

Revision ID: 26961e75e149
Revises: 9f72b1fd8552, abc1234567def89
Create Date: 2026-04-04 18:06:14.938149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26961e75e149'
down_revision: Union[str, Sequence[str], None] = ('9f72b1fd8552', 'abc1234567def89')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
