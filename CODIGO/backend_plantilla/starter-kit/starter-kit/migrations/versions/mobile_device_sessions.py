"""Add device_sessions table for mobile authentication

Revision ID: mobile_device_sessions
Revises: 
Create Date: 2026-04-16

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'mobile_device_sessions'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create device_sessions table
    op.create_table(
        'device_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('device_id', sa.String(), nullable=False),
        sa.Column('device_name', sa.String(), nullable=True),
        sa.Column('device_type', sa.String(), nullable=False),
        sa.Column('os', sa.String(), nullable=True),
        sa.Column('os_version', sa.String(), nullable=True),
        sa.Column('app_version', sa.String(), nullable=True),
        sa.Column('device_token', sa.String(), nullable=True),
        sa.Column('refresh_token', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('last_accessed', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('device_id')
    )
    
    # Create indexes for better query performance
    op.create_index(op.f('ix_device_sessions_device_id'), 'device_sessions', ['device_id'], unique=True)
    op.create_index(op.f('ix_device_sessions_user_id'), 'device_sessions', ['user_id'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_device_sessions_user_id'), table_name='device_sessions')
    op.drop_index(op.f('ix_device_sessions_device_id'), table_name='device_sessions')
    
    # Drop table
    op.drop_table('device_sessions')
