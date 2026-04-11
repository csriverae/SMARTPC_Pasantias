"""Add new columns for SaaS features

Revision ID: add_saas_columns_001
Revises: b790dd0fbced
Create Date: 2026-04-10 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'add_saas_columns_001'
down_revision = 'b790dd0fbced'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add phone and address to users table
    op.add_column('users', sa.Column('phone', sa.String(), nullable=True))
    op.add_column('users', sa.Column('address', sa.String(), nullable=True))
    
    # Add generated_password to user_invitations table (note: plural)
    op.add_column('user_invitations', sa.Column('generated_password', sa.String(), nullable=True))
    
    # Add columns to agreements table (note: plural)
    op.add_column('agreements', sa.Column('payment_type', sa.String(), nullable=True, server_default='prepaid'))
    op.add_column('agreements', sa.Column('daily_budget', sa.Float(), nullable=True))
    op.add_column('agreements', sa.Column('discount_percentage', sa.Float(), nullable=True))
    op.add_column('agreements', sa.Column('normal_price', sa.Float(), nullable=True))
    op.add_column('agreements', sa.Column('discount_price', sa.Float(), nullable=True))
    op.add_column('agreements', sa.Column('company_percentage', sa.Float(), nullable=True))
    op.add_column('agreements', sa.Column('employee_percentage', sa.Float(), nullable=True))
    op.add_column('agreements', sa.Column('meal_price', sa.Float(), nullable=True))
    op.add_column('agreements', sa.Column('notes', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove columns from agreements table
    op.drop_column('agreements', 'notes')
    op.drop_column('agreements', 'meal_price')
    op.drop_column('agreements', 'employee_percentage')
    op.drop_column('agreements', 'company_percentage')
    op.drop_column('agreements', 'discount_price')
    op.drop_column('agreements', 'normal_price')
    op.drop_column('agreements', 'discount_percentage')
    op.drop_column('agreements', 'daily_budget')
    op.drop_column('agreements', 'payment_type')
    
    # Remove columns from user_invitations table
    op.drop_column('user_invitations', 'generated_password')
    
    # Remove columns from users table
    op.drop_column('users', 'address')
    op.drop_column('users', 'phone')
